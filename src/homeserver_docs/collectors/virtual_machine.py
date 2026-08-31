"""Proxmox virtual machine collector."""

from __future__ import annotations

import re
from dataclasses import replace

from homeserver_docs.config import load_config
from homeserver_docs.models.virtual_machine import (
    VirtualDisk,
    VirtualMachine,
    VirtualNetworkInterface,
)
from homeserver_docs.parsers.virtual_machine import parse_qm_list
from homeserver_docs.parsers.virtual_machine_config import parse_qm_config
from homeserver_docs.utils.ssh import SSHConnection


class VirtualMachineCollector:
    """Collect Proxmox virtual machine information."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[VirtualMachine]:
        """Collect VM list and configuration details."""

        output = self.connection.run("qm list")
        virtual_machines = parse_qm_list(output)

        enriched: list[VirtualMachine] = []

        for vm in virtual_machines:
            config_output = self.connection.run(
                f"qm config {vm.vmid}"
            )
            config = parse_qm_config(config_output)

            disks = self._parse_disks(config)
            networks = self._parse_networks(config)

            storage = sorted(
                {
                    disk.storage
                    for disk in disks
                    if disk.storage
                }
            )

            tags = [
                tag.strip()
                for tag in config.get("tags", "").split(";")
                if tag.strip()
            ]

            enriched.append(
                replace(
                    vm,
                    cpu_cores=self._parse_int(
                        config.get("cores")
                    ) or 0,
                    memory_mb=self._parse_int(
                        config.get("memory")
                    ) or vm.memory_mb,
                    storage=storage,
                    disks=disks,
                    network_interfaces=networks,
                    guest_os=config.get("ostype"),
                    description=config.get("description"),
                    tags=tags,
                    startup_order=self._parse_startup_order(
                        config.get("startup")
                    ),
                )
            )

        return enriched

    @staticmethod
    def _parse_int(value: str | None) -> int | None:
        """Convert a value to integer when possible."""

        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def _parse_disks(
        config: dict[str, str],
    ) -> list[VirtualDisk]:
        """Extract VM disks from qm config."""

        disks: list[VirtualDisk] = []

        for key, value in config.items():
            if not re.fullmatch(
                r"(scsi|sata|virtio|ide)\d+",
                key,
            ):
                continue

            if "media=cdrom" in value or value == "none":
                continue

            first_part = value.split(",", 1)[0]

            if ":" not in first_part:
                continue

            storage, volume = first_part.split(":", 1)

            size_match = re.search(
                r"(?:^|,)size=([\d.]+)([GMT])(?:,|$)",
                value,
            )

            size_gb: float | None = None

            if size_match:
                size = float(size_match.group(1))
                unit = size_match.group(2)

                if unit == "M":
                    size_gb = size / 1024
                elif unit == "G":
                    size_gb = size
                elif unit == "T":
                    size_gb = size * 1024

            disks.append(
                VirtualDisk(
                    interface=key,
                    storage=storage,
                    volume=volume,
                    size_gb=size_gb,
                )
            )

        return disks

    @staticmethod
    def _parse_networks(
        config: dict[str, str],
    ) -> list[VirtualNetworkInterface]:
        """Extract VM network interfaces from qm config."""

        interfaces: list[VirtualNetworkInterface] = []

        for key, value in config.items():
            if not re.fullmatch(r"net\d+", key):
                continue

            parts = value.split(",")
            first_part = parts[0]

            model = first_part
            mac_address: str | None = None

            if "=" in first_part:
                model, mac_address = first_part.split("=", 1)

            bridge: str | None = None

            for part in parts[1:]:
                if part.startswith("bridge="):
                    bridge = part.split("=", 1)[1]

            interfaces.append(
                VirtualNetworkInterface(
                    interface=key,
                    model=model,
                    bridge=bridge,
                    mac_address=mac_address,
                )
            )

        return interfaces

    @staticmethod
    def _parse_startup_order(
        value: str | None,
    ) -> int | None:
        """Extract startup order."""

        if not value:
            return None

        match = re.search(r"order=(\d+)", value)

        if not match:
            return None

        return int(match.group(1))
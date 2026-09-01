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
from homeserver_docs.parsers.guest_network import parse_guest_ipv4_addresses
from homeserver_docs.parsers.snapshot import parse_qm_snapshots
from homeserver_docs.parsers.virtual_machine import parse_qm_list
from homeserver_docs.parsers.virtual_machine_config import parse_qm_config
from homeserver_docs.parsers.vm_status import parse_vm_uptime
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

            snapshots = self._collect_snapshots(vm.vmid)

            ip_addresses: list[str] = []

            if vm.status == "running" and config.get("agent"):
                try:
                    guest_output = self.connection.run(
                        f"qm guest cmd {vm.vmid} "
                        "network-get-interfaces"
                    )
                    ip_addresses = parse_guest_ipv4_addresses(
                        guest_output
                    )
                except RuntimeError:
                    ip_addresses = []

            uptime: str | None = None

            if vm.status == "running":
                uptime = self._collect_uptime(vm.vmid)

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
                    ip_addresses=ip_addresses,
                    guest_os=config.get("ostype"),
                    description=config.get("description"),
                    tags=tags,
                    snapshots=snapshots,
                    startup_order=self._parse_startup_order(
                        config.get("startup")
                    ),
                    uptime=uptime,
                )
            )

        return enriched

    def _collect_snapshots(self, vmid: int) -> list[str]:
        """Collect snapshot names for a VM."""

        try:
            output = self.connection.run(
                f"qm listsnapshot {vmid}"
            )
        except RuntimeError:
            return []

        return parse_qm_snapshots(output)

    def _collect_uptime(self, vmid: int) -> str | None:
        """Collect and format VM uptime."""

        try:
            output = self.connection.run(
                f"qm status {vmid} --verbose"
            )
        except RuntimeError:
            return None

        seconds = parse_vm_uptime(output)

        if seconds is None:
            return None

        return self._format_uptime(seconds)

    @staticmethod
    def _format_uptime(seconds: int) -> str:
        """Convert uptime seconds to a readable value."""

        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        parts: list[str] = []

        if days:
            parts.append(f"{days} d")

        if hours:
            parts.append(f"{hours} u")

        if minutes or not parts:
            parts.append(f"{minutes} min")

        return " ".join(parts)

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
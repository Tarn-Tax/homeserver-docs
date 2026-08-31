"""Proxmox LXC container collector."""

from __future__ import annotations

import re
from dataclasses import replace

from homeserver_docs.config import load_config
from homeserver_docs.models.container import Container
from homeserver_docs.parsers.container import parse_pct_list
from homeserver_docs.parsers.container_config import parse_pct_config
from homeserver_docs.utils.ssh import SSHConnection


class ContainerCollector:
    """Collect Proxmox LXC container information."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[Container]:
        """Collect LXC containers and enrich them with configuration details."""

        output = self.connection.run("pct list")
        containers = parse_pct_list(output)

        enriched_containers: list[Container] = []

        for container in containers:
            config_output = self.connection.run(
                f"pct config {container.vmid}"
            )
            config = parse_pct_config(config_output)

            root_disk_gb = self._parse_root_disk_size(
                config.get("rootfs")
            )

            network_interfaces = [
                value
                for key, value in config.items()
                if key.startswith("net")
            ]

            mountpoints = [
                value
                for key, value in config.items()
                if key.startswith("mp")
            ]

            tags = [
                tag.strip()
                for tag in config.get("tags", "").split(";")
                if tag.strip()
            ]

            enriched_containers.append(
                replace(
                    container,
                    memory_mb=self._parse_int(config.get("memory")),
                    swap_mb=self._parse_int(config.get("swap")),
                    root_disk_gb=root_disk_gb,
                    cpu_cores=self._parse_int(config.get("cores")),
                    network_interfaces=network_interfaces,
                    mountpoints=mountpoints,
                    tags=tags,
                    startup_order=self._parse_startup_order(
                        config.get("startup")
                    ),
                    description=config.get("description"),
                )
            )

        return enriched_containers

    @staticmethod
    def _parse_int(value: str | None) -> int | None:
        """Convert a value to an integer when possible."""

        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def _parse_root_disk_size(value: str | None) -> float | None:
        """Extract the root disk size in GiB."""

        if not value:
            return None

        match = re.search(r"size=([\d.]+)([GM])", value)
        if not match:
            return None

        size = float(match.group(1))
        unit = match.group(2)

        if unit == "M":
            return size / 1024

        return size

    @staticmethod
    def _parse_startup_order(value: str | None) -> int | None:
        """Extract the startup order from a Proxmox startup value."""

        if not value:
            return None

        match = re.search(r"order=(\d+)", value)
        if not match:
            return None

        return int(match.group(1))
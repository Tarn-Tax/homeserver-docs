"""Proxmox network collector."""

from __future__ import annotations

from homeserver_docs.config import load_config
from homeserver_docs.models.network import NetworkInterface
from homeserver_docs.parsers.network import parse_network_interfaces
from homeserver_docs.utils.ssh import SSHConnection


class NetworkCollector:
    """Collect Proxmox network configuration."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[NetworkInterface]:
        """Collect and parse /etc/network/interfaces."""

        output = self.connection.run("cat /etc/network/interfaces")
        return parse_network_interfaces(output)
"""Proxmox virtual machine collector."""

from __future__ import annotations

from homeserver_docs.config import load_config
from homeserver_docs.models.virtual_machine import VirtualMachine
from homeserver_docs.parsers.virtual_machine import parse_qm_list
from homeserver_docs.utils.ssh import SSHConnection


class VirtualMachineCollector:
    """Collect Proxmox virtual machine information."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[VirtualMachine]:
        """Collect and parse `qm list`."""

        output = self.connection.run("qm list")
        return parse_qm_list(output)
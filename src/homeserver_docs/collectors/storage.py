"""Proxmox storage collector."""

from __future__ import annotations

from homeserver_docs.config import load_config
from homeserver_docs.models.storage import Storage
from homeserver_docs.parsers.storage import parse_storage_status
from homeserver_docs.utils.ssh import SSHConnection


class StorageCollector:
    """Collect Proxmox storage information."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[Storage]:
        """Collect and parse `pvesm status`."""

        output = self.connection.run("pvesm status")
        return parse_storage_status(output)
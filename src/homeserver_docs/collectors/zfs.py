"""ZFS collector."""

from __future__ import annotations

from homeserver_docs.config import load_config
from homeserver_docs.models.zfs import ZfsPool
from homeserver_docs.parsers.zfs import parse_zpool_status
from homeserver_docs.utils.ssh import SSHConnection


class ZfsCollector:
    """Collect ZFS pool health information."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[ZfsPool]:
        """Collect ZFS pool status."""

        output = self.connection.run("zpool status")

        return parse_zpool_status(output)
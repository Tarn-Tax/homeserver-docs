"""Proxmox host collector."""

from __future__ import annotations

from homeserver_docs.config import load_config
from homeserver_docs.models.host import Host
from homeserver_docs.utils.ssh import SSHConnection


class HostCollector:
    """Collect information about the Proxmox host."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> Host:
        """Collect host information through SSH."""

        hostname = self.connection.run("hostname")
        proxmox_version = self.connection.run("pveversion")
        kernel = self.connection.run("uname -r")

        cpu_model = self.connection.run(
            "lscpu | sed -n 's/^Model name:[[:space:]]*//p'"
        )
        cpu_cores = int(self.connection.run("nproc"))
        memory_total = self.connection.run(
            "free -h | awk '/^Mem:/ {print $2}'"
        )
        uptime = self.connection.run("uptime -p")

        return Host(
            hostname=hostname,
            proxmox_version=proxmox_version,
            kernel=kernel,
            cpu_model=cpu_model,
            cpu_cores=cpu_cores,
            memory_total=memory_total,
            uptime=uptime,
        )
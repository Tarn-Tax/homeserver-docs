"""
Host collector.
"""

from __future__ import annotations

import os
import platform

from homeserver_docs.models.host import Host
from homeserver_docs.utils.command import CommandRunner


class HostCollector:
    """Collect information about the Proxmox host."""

    def __init__(self) -> None:
        self.runner = CommandRunner()

    def collect(self) -> Host:
        """Collect host information."""

        hostname = self.runner.run(["hostname"])

        try:
            version = self.runner.run(["pveversion"]).split()[1]
        except Exception:
            version = "unknown"

        kernel = platform.release()

        try:
            cpu_model = platform.processor() or "unknown"
        except Exception:
            cpu_model = "unknown"

        cpu_cores = os.cpu_count() or 0

        memory_total = "unknown"
        uptime = "unknown"

        return Host(
            hostname=hostname,
            proxmox_version=version,
            kernel=kernel,
            cpu_model=cpu_model,
            cpu_cores=cpu_cores,
            memory_total=memory_total,
            uptime=uptime,
        )
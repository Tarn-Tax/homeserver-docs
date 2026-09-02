"""Physical disk collector."""

from __future__ import annotations

from dataclasses import replace

from homeserver_docs.config import load_config
from homeserver_docs.models.disk import PhysicalDisk
from homeserver_docs.parsers.smart import parse_smart_info
from homeserver_docs.utils.ssh import SSHConnection


class DiskCollector:
    """Collect physical disks from the Proxmox host."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().proxmox)

        self.connection = connection

    def collect(self) -> list[PhysicalDisk]:
        """Collect physical disk and SMART information."""

        output = self.connection.run(
            "lsblk -d -n -o NAME,MODEL,SERIAL,SIZE,TYPE"
        )

        disks: list[PhysicalDisk] = []

        for line in output.splitlines():
            parts = line.split()

            if len(parts) < 5 or parts[-1] != "disk":
                continue

            device = f"/dev/{parts[0]}"
            size = parts[-2]
            serial = parts[-3]
            model = " ".join(parts[1:-3])

            disk = PhysicalDisk(
                device=device,
                model=model or None,
                serial=serial or None,
                size=size,
            )

            try:
                smart_output = self.connection.run(
                    f"smartctl -a {device}"
                )
                smart = parse_smart_info(smart_output)

                disk = replace(
                    disk,
                    smart_status=smart["smart_status"],
                    temperature_c=smart["temperature_c"],
                    power_on_hours=smart["power_on_hours"],
                )
            except RuntimeError:
                pass

            disks.append(disk)

        return disks
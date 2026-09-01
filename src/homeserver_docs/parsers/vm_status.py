"""Virtual machine status parser."""

from __future__ import annotations


def parse_vm_uptime(output: str) -> int | None:
    """Extract VM uptime in seconds from `qm status --verbose`."""

    for line in output.splitlines():
        line = line.strip()

        if not line.startswith("uptime:"):
            continue

        _, value = line.split(":", 1)

        try:
            return int(value.strip())
        except ValueError:
            return None

    return None
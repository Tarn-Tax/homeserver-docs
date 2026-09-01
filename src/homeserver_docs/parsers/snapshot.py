"""Proxmox snapshot parser."""

from __future__ import annotations

import re


def parse_qm_snapshots(output: str) -> list[str]:
    """Extract snapshot names from qm listsnapshot output."""

    snapshots: list[str] = []

    for line in output.splitlines():
        match = re.search(r"[>`-]+\s+(\S+)", line)

        if not match:
            continue

        name = match.group(1)

        if name == "current":
            continue

        snapshots.append(name)

    return snapshots
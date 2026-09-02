"""Proxmox backup parser."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone


def parse_latest_backups(output: str) -> dict[int, str]:
    """Return the latest backup timestamp per VM."""

    items = json.loads(output)

    backups: dict[int, list[int]] = defaultdict(list)

    for item in items:
        vmid = item.get("vmid")
        ctime = item.get("ctime")

        if vmid is None or ctime is None:
            continue

        backups[int(vmid)].append(int(ctime))

    latest: dict[int, str] = {}

    for vmid, timestamps in backups.items():
        newest = max(timestamps)

        latest[vmid] = datetime.fromtimestamp(
            newest,
            tz=timezone.utc,
        ).astimezone().strftime("%Y-%m-%d %H:%M")

    return latest
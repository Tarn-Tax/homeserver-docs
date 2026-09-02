"""ZFS status parser."""

from __future__ import annotations

import re

from homeserver_docs.models.zfs import ZfsDevice, ZfsPool


def parse_zpool_status(output: str) -> list[ZfsPool]:
    """Parse output from `zpool status`."""

    pools: list[ZfsPool] = []

    blocks = re.split(r"(?=^\s*pool:\s)", output, flags=re.MULTILINE)

    for block in blocks:
        if not block.strip():
            continue

        pool_match = re.search(r"^\s*pool:\s+(.+)$", block, re.MULTILINE)
        state_match = re.search(r"^\s*state:\s+(.+)$", block, re.MULTILINE)

        if not pool_match or not state_match:
            continue

        name = pool_match.group(1).strip()
        state = state_match.group(1).strip()

        status_match = re.search(
            r"^\s*status:\s+(.+?)(?=^\s*(?:action|see|scan|config):)",
            block,
            flags=re.MULTILINE | re.DOTALL,
        )

        status_message = None

        if status_match:
            status_message = " ".join(
                status_match.group(1).split()
            )

        error_match = re.search(
            r"^\s*errors:\s+(.+)$",
            block,
            re.MULTILINE,
        )

        data_errors = (
            error_match.group(1).strip()
            if error_match
            else None
        )

        devices: list[ZfsDevice] = []

        for line in block.splitlines():
            parts = line.split()

            if len(parts) != 5:
                continue

            if parts[1] not in {
                "ONLINE",
                "DEGRADED",
                "FAULTED",
                "OFFLINE",
                "UNAVAIL",
                "REMOVED",
            }:
                continue

            try:
                read_errors = int(parts[2])
                write_errors = int(parts[3])
                checksum_errors = int(parts[4])
            except ValueError:
                continue

            devices.append(
                ZfsDevice(
                    name=parts[0],
                    state=parts[1],
                    read_errors=read_errors,
                    write_errors=write_errors,
                    checksum_errors=checksum_errors,
                )
            )

        pools.append(
            ZfsPool(
                name=name,
                state=state,
                status_message=status_message,
                data_errors=data_errors,
                devices=devices,
            )
        )

    return pools
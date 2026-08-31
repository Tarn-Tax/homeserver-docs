"""LXC container parser."""

from __future__ import annotations

from homeserver_docs.models.container import Container


def parse_pct_list(output: str) -> list[Container]:
    """Parse the output of `pct list`."""

    lines = [line for line in output.splitlines() if line.strip()]
    if len(lines) < 2:
        return []

    containers: list[Container] = []

    for line in lines[1:]:
        parts = line.split()

        if len(parts) < 3:
            continue

        vmid = int(parts[0])
        status = parts[1]
        name = parts[-1]

        containers.append(
            Container(
                vmid=vmid,
                name=name,
                status=status,
            )
        )

    return containers
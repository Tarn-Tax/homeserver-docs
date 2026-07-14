"""Storage parser."""

from __future__ import annotations

from homeserver_docs.models.storage import Storage


def parse_storage_status(output: str) -> list[Storage]:
    """Parse the output of `pvesm status`."""

    lines = [line for line in output.splitlines() if line.strip()]
    if len(lines) < 2:
        return []

    storage_items: list[Storage] = []

    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 7:
            continue

        storage_items.append(
            Storage(
                name=parts[0],
                storage_type=parts[1],
                status=parts[2],
                total_kib=int(parts[3]),
                used_kib=int(parts[4]),
                available_kib=int(parts[5]),
                usage_percent=float(parts[6].rstrip("%")),
            )
        )

    return storage_items
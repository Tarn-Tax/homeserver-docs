"""Virtual machine configuration parser."""

from __future__ import annotations


def parse_qm_config(output: str) -> dict[str, str]:
    """Parse the output of `qm config <vmid>`."""

    config: dict[str, str] = {}

    for line in output.splitlines():
        if not line.strip() or ":" not in line:
            continue

        key, value = line.split(":", 1)
        config[key.strip()] = value.strip()

    return config
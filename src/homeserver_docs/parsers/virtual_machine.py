"""Virtual machine parser."""

from __future__ import annotations

from homeserver_docs.models.virtual_machine import VirtualMachine


def parse_qm_list(output: str) -> list[VirtualMachine]:
    """Parse the output of `qm list`."""

    lines = [line for line in output.splitlines() if line.strip()]

    if len(lines) < 2:
        return []

    virtual_machines: list[VirtualMachine] = []

    for line in lines[1:]:
        parts = line.split()

        if len(parts) < 6:
            continue

        virtual_machines.append(
            VirtualMachine(
                vmid=int(parts[0]),
                name=parts[1],
                status=parts[2],
                cpu_cores=0,
                memory_mb=int(parts[3]),
                boot_disk_gb=float(parts[4]),
                pid=int(parts[5]),
            )
        )

    return virtual_machines
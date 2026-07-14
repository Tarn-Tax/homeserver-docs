"""Markdown renderer."""

from __future__ import annotations

from pathlib import Path

from homeserver_docs.models.homeserver import Homeserver
from homeserver_docs.models.storage import Storage

from homeserver_docs.models.virtual_machine import VirtualMachine

def format_kib(value: int) -> str:
    """Convert KiB to a readable unit."""

    units = ["KiB", "MiB", "GiB", "TiB"]
    size = float(value)
    unit = units[0]

    for unit in units:
        if size < 1024 or unit == units[-1]:
            break
        size /= 1024

    return f"{size:.1f} {unit}"


def render_storage_table(storage_items: list[Storage]) -> str:
    """Render storage items as a Markdown table."""

    if not storage_items:
        return "Geen storage gevonden."

    rows = [
        "| Naam | Type | Status | Totaal | Gebruikt | Vrij | Gebruik |",
        "|---|---|---|---:|---:|---:|---:|",
    ]

    for item in storage_items:
        rows.append(
            "| "
            f"{item.name} | "
            f"{item.storage_type} | "
            f"{item.status} | "
            f"{format_kib(item.total_kib)} | "
            f"{format_kib(item.used_kib)} | "
            f"{format_kib(item.available_kib)} | "
            f"{item.usage_percent:.2f}% |"
        )
    
    return "\n".join(rows)

def render_virtual_machine_table(virtual_machines: list[VirtualMachine]) -> str:
    """Render virtual machines as a Markdown table."""

    if not virtual_machines:
        return "Geen virtuele machines gevonden."

    rows = [
        "| VMID | Naam | Status | RAM | Bootdisk | PID |",
        "|---:|---|---|---:|---:|---:|",
    ]

    for vm in virtual_machines:
        rows.append(
            "| "
            f"{vm.vmid} | "
            f"{vm.name} | "
            f"{vm.status} | "
            f"{vm.memory_mb} MB | "
            f"{vm.boot_disk_gb:.1f} GB | "
            f"{vm.pid} |"
        )

    return "\n".join(rows)


class MarkdownRenderer:
    """Render a complete homeserver inventory."""

    def render(self, homeserver: Homeserver, output_dir: Path) -> Path:
        """Render the complete inventory to Markdown."""

        output_dir.mkdir(parents=True, exist_ok=True)
        target = output_dir / "Homeserver.md"

        host = homeserver.host
        storage_table = render_storage_table(homeserver.storage)

        markdown = f"""# Homeserver

## Proxmox-host

| Eigenschap | Waarde |
|---|---|
| Hostname | {host.hostname} |
| Proxmox | {host.proxmox_version} |
| Kernel | {host.kernel} |
| CPU | {host.cpu_model} |
| Cores | {host.cpu_cores} |
| Geheugen | {host.memory_total} |
| Uptime | {host.uptime} |

## Storage

{storage_table}
"""

        target.write_text(markdown, encoding="utf-8")
        return target

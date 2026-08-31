"""Markdown renderer."""

from __future__ import annotations

from pathlib import Path

from homeserver_docs.models.container import Container
from homeserver_docs.models.homeserver import Homeserver
from homeserver_docs.models.network import NetworkInterface
from homeserver_docs.models.storage import Storage
from homeserver_docs.models.virtual_machine import VirtualMachine


def format_kib(value: int) -> str:
    """Convert KiB to a readable unit."""

    units = ["KiB", "MiB", "GiB", "TiB"]
    size = float(value)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} TiB"


def format_optional(value: object | None, suffix: str = "") -> str:
    """Format an optional value."""

    if value is None:
        return "-"

    return f"{value}{suffix}"


def render_storage_table(storage_items: list[Storage]) -> str:
    """Render storage as Markdown."""

    if not storage_items:
        return "Geen storage gevonden."

    rows = [
        "| Naam | Type | Status | Totaal | Gebruikt | Vrij | Gebruik |",
        "|---|---|---|---:|---:|---:|---:|",
    ]

    for item in storage_items:
        rows.append(
            f"| {item.name} "
            f"| {item.storage_type} "
            f"| {item.status} "
            f"| {format_kib(item.total_kib)} "
            f"| {format_kib(item.used_kib)} "
            f"| {format_kib(item.available_kib)} "
            f"| {item.usage_percent:.2f}% |"
        )

    return "\n".join(rows)


def render_virtual_machine_table(
    virtual_machines: list[VirtualMachine],
) -> str:
    """Render virtual machines as Markdown."""

    if not virtual_machines:
        return "Geen virtuele machines gevonden."

    rows = [
        "| VMID | Naam | Status | RAM | Bootdisk | PID |",
        "|---:|---|---|---:|---:|---:|",
    ]

    for vm in virtual_machines:
        rows.append(
            f"| {vm.vmid} "
            f"| {vm.name} "
            f"| {vm.status} "
            f"| {vm.memory_mb} MB "
            f"| {vm.boot_disk_gb:.1f} GB "
            f"| {vm.pid} |"
        )

    return "\n".join(rows)


def render_container_table(containers: list[Container]) -> str:
    """Render LXC containers as Markdown."""

    if not containers:
        return "Geen LXC-containers gevonden."

    rows = [
        "| CTID | Naam | Status | CPU | RAM | Swap | Rootdisk | Netwerk | Tags |",
        "|---:|---|---|---:|---:|---:|---:|---|---|",
    ]

    for container in containers:
        networks = "<br>".join(container.network_interfaces) or "-"
        tags = ", ".join(container.tags) or "-"

        rows.append(
            f"| {container.vmid} "
            f"| {container.name} "
            f"| {container.status} "
            f"| {format_optional(container.cpu_cores)} "
            f"| {format_optional(container.memory_mb, ' MB')} "
            f"| {format_optional(container.swap_mb, ' MB')} "
            f"| {format_optional(container.root_disk_gb, ' GB')} "
            f"| {networks} "
            f"| {tags} |"
        )

    return "\n".join(rows)


def render_network_table(networks: list[NetworkInterface]) -> str:
    """Render Proxmox network configuration as Markdown."""

    if not networks:
        return "Geen netwerkinterfaces gevonden."

    rows = [
        "| Naam | Type | Methode | Adres | Gateway | Bridge-poorten | Omschrijving |",
        "|---|---|---|---|---|---|---|",
    ]

    for network in networks:
        rows.append(
            f"| {network.name} "
            f"| {network.interface_type} "
            f"| {network.method} "
            f"| {network.address or '-'} "
            f"| {network.gateway or '-'} "
            f"| {network.bridge_ports or '-'} "
            f"| {network.comment or '-'} |"
        )

    return "\n".join(rows)


class MarkdownRenderer:
    """Render the complete homeserver inventory."""

    def render(
        self,
        homeserver: Homeserver,
        output_dir: Path,
    ) -> Path:
        """Render the inventory to Markdown."""

        output_dir.mkdir(parents=True, exist_ok=True)
        target = output_dir / "Homeserver.md"

        host = homeserver.host

        vm_count = len(homeserver.virtual_machines)
        container_count = len(homeserver.containers)
        storage_count = len(homeserver.storage)
        network_count = len(homeserver.networks)

        storage_table = render_storage_table(homeserver.storage)
        vm_table = render_virtual_machine_table(
            homeserver.virtual_machines
        )
        container_table = render_container_table(
            homeserver.containers
        )
        network_table = render_network_table(
            homeserver.networks
        )

        markdown = f"""# Homeserver

## Samenvatting

| Onderdeel | Waarde |
|---|---|
| Host | {host.hostname} |
| Proxmox | {host.proxmox_version} |
| Virtuele machines | {vm_count} |
| LXC-containers | {container_count} |
| Storage locaties | {storage_count} |
| Netwerkinterfaces | {network_count} |
| Laatste inventarisatie | Nog niet beschikbaar |

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

## Virtuele machines

{vm_table}

## LXC-containers

{container_table}

## Netwerk

{network_table}
"""

        target.write_text(markdown, encoding="utf-8")

        return target
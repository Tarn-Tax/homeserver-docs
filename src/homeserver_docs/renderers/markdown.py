"""Markdown renderer."""

from __future__ import annotations

from pathlib import Path

from datetime import datetime

from homeserver_docs.models.container import Container
from homeserver_docs.models.disk import PhysicalDisk
from homeserver_docs.models.docker import DockerContainer
from homeserver_docs.models.docker_stack import DockerStack
from homeserver_docs.models.homeserver import Homeserver
from homeserver_docs.models.network import NetworkInterface
from homeserver_docs.models.storage import Storage
from homeserver_docs.models.virtual_machine import VirtualMachine
from homeserver_docs.models.zfs import ZfsPool


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
        "| VMID | Naam | Status | CPU | RAM | OS | IP-adres | Uptime | Storage | Netwerk | Tags | Snapshots | Laatste back-up |",
        "|---:|---|---|---:|---:|---|---|---|---|---|---|---|---|",
    ]

    for vm in virtual_machines:
        storage = ", ".join(vm.storage) or "-"
        ip_addresses = ", ".join(vm.ip_addresses) or "-"
        uptime = vm.uptime or "-"
        backup = vm.backup_status or "-"

        networks: list[str] = []

        for interface in vm.network_interfaces:
            network = interface.interface

            if interface.bridge:
                network += f" → {interface.bridge}"

            if interface.mac_address:
                network += f" ({interface.mac_address})"

            networks.append(network)

        network_text = "<br>".join(networks) or "-"
        tags = ", ".join(vm.tags) or "-"
        snapshots = ", ".join(vm.snapshots) or "-"

        rows.append(
            f"| {vm.vmid} "
            f"| {vm.name} "
            f"| {vm.status} "
            f"| {vm.cpu_cores} "
            f"| {vm.memory_mb} MB "
            f"| {vm.guest_os or '-'} "
            f"| {ip_addresses} "
            f"| {uptime} "
            f"| {storage} "
            f"| {network_text} "
            f"| {tags} "
            f"| {snapshots} "
            f"| {backup} |"
        )

    return "\n".join(rows)


def render_container_table(containers: list[Container]) -> str:
    """Render LXC containers as Markdown."""

    if not containers:
        return "Geen LXC-containers gevonden."

    rows = [
        "| CTID | Naam | Status | CPU | RAM | Swap | Rootdisk | Netwerk | Tags | Snapshots | Laatste back-up |",
        "|---:|---|---|---:|---:|---:|---:|---|---|---|---|",
    ]

    for container in containers:
        networks = "<br>".join(container.network_interfaces) or "-"
        tags = ", ".join(container.tags) or "-"
        snapshots = ", ".join(container.snapshots) or "-"
        backup = container.backup_status or "-"

        rows.append(
            f"| {container.vmid} "
            f"| {container.name} "
            f"| {container.status} "
            f"| {format_optional(container.cpu_cores)} "
            f"| {format_optional(container.memory_mb, ' MB')} "
            f"| {format_optional(container.swap_mb, ' MB')} "
            f"| {format_optional(container.root_disk_gb, ' GB')} "
            f"| {networks} "
            f"| {tags} "
            f"| {snapshots} "
            f"| {backup} |"
        )

    return "\n".join(rows)


def render_network_table(
    networks: list[NetworkInterface],
) -> str:
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


def render_zfs_table(zfs_pools: list[ZfsPool]) -> str:
    """Render ZFS pool health as Markdown."""

    if not zfs_pools:
        return "Geen ZFS-pools gevonden."

    rows = [
        "| Pool | Status | Gezond | Device | READ | WRITE | CKSUM | Datafouten |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]

    for pool in zfs_pools:
        health = "OK" if pool.healthy else "WAARSCHUWING"

        if not pool.devices:
            rows.append(
                f"| {pool.name} "
                f"| {pool.state} "
                f"| {health} "
                f"| - | 0 | 0 | 0 "
                f"| {pool.data_errors or '-'} |"
            )
            continue

        for index, device in enumerate(pool.devices):
            pool_name = pool.name if index == 0 else ""
            pool_state = pool.state if index == 0 else ""
            pool_health = health if index == 0 else ""
            data_errors = (
                pool.data_errors or "-"
                if index == 0
                else ""
            )

            rows.append(
                f"| {pool_name} "
                f"| {pool_state} "
                f"| {pool_health} "
                f"| {device.name} "
                f"| {device.read_errors} "
                f"| {device.write_errors} "
                f"| {device.checksum_errors} "
                f"| {data_errors} |"
            )

    return "\n".join(rows)


def render_zfs_warnings(zfs_pools: list[ZfsPool]) -> str:
    """Render warnings for unhealthy ZFS pools."""

    warnings: list[str] = []

    for pool in zfs_pools:
        if pool.healthy:
            continue

        warnings.append(
            f"- **ZFS-pool {pool.name}: controle vereist.**"
        )

        for device in pool.devices:
            if (
                device.read_errors
                or device.write_errors
                or device.checksum_errors
            ):
                warnings.append(
                    f"  - `{device.name}`: "
                    f"READ={device.read_errors}, "
                    f"WRITE={device.write_errors}, "
                    f"CKSUM={device.checksum_errors}"
                )

    if not warnings:
        return "Geen actuele ZFS-waarschuwingen."

    return "\n".join(warnings)


def render_disk_table(disks: list[PhysicalDisk]) -> str:
    """Render physical disks and SMART information."""

    if not disks:
        return "Geen fysieke disks gevonden."

    rows = [
        "| Device | Model | Serienummer | Grootte | SMART | Temperatuur | Draaiuren |",
        "|---|---|---|---:|---|---:|---:|",
    ]

    for disk in disks:
        temperature = (
            f"{disk.temperature_c} °C"
            if disk.temperature_c is not None
            else "-"
        )

        power_on_hours = (
            f"{disk.power_on_hours} uur"
            if disk.power_on_hours is not None
            else "-"
        )

        rows.append(
            f"| {disk.device} "
            f"| {disk.model or '-'} "
            f"| {disk.serial or '-'} "
            f"| {disk.size or '-'} "
            f"| {disk.smart_status or '-'} "
            f"| {temperature} "
            f"| {power_on_hours} |"
        )

    return "\n".join(rows)


def render_disk_warnings(disks: list[PhysicalDisk]) -> str:
    """Render SMART and temperature warnings."""

    warnings: list[str] = []

    for disk in disks:
        if (
            disk.smart_status
            and disk.smart_status.upper() != "PASSED"
        ):
            warnings.append(
                f"- **SMART-waarschuwing voor {disk.device}: "
                f"{disk.smart_status}.**"
            )

        if (
            disk.temperature_c is not None
            and disk.temperature_c >= 60
        ):
            warnings.append(
                f"- **Hoge temperatuur op {disk.device}: "
                f"{disk.temperature_c} °C.**"
            )

    if not warnings:
        return "Geen actuele SMART-waarschuwingen."

    return "\n".join(warnings)

def render_docker_table(
    containers: list[DockerContainer],
) -> str:
    """Render Docker containers as Markdown."""

    if not containers:
        return "Geen Docker-containers gevonden."

    rows = [
        "| Naam | Image | Status | Health | Poorten | Netwerk | Compose-project | Service |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for container in containers:
        rows.append(
            f"| {container.name} "
            f"| {container.image} "
            f"| {container.status} "
            f"| {container.health or '-'} "
            f"| {container.ports or '-'} "
            f"| {container.networks or '-'} "
            f"| {container.compose_project or '-'} "
            f"| {container.compose_service or '-'} |"
        )

    return "\n".join(rows)

def render_docker_stack_table(
    stacks: list[DockerStack],
) -> str:
    """Render Docker Compose stacks as Markdown."""

    if not stacks:
        return "Geen Docker Compose-stacks gevonden."

    rows = [
        "| Stack | Containers | Draaiend | Healthy | Compose-bestand |",
        "|---|---|---:|---:|---|",
    ]

    for stack in stacks:
        containers = "<br>".join(stack.containers) or "-"

        rows.append(
            f"| {stack.name} "
            f"| {containers} "
            f"| {stack.running_count} "
            f"| {stack.healthy_count} "
            f"| {stack.compose_file or '-'} |"
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
        inventory_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        vm_count = len(homeserver.virtual_machines)
        container_count = len(homeserver.containers)
        storage_count = len(homeserver.storage)
        network_count = len(homeserver.networks)
        zfs_pool_count = len(homeserver.zfs_pools)
        physical_disk_count = len(homeserver.physical_disks)
        docker_count = len(homeserver.docker_containers)

        storage_table = render_storage_table(
            homeserver.storage
        )

        vm_table = render_virtual_machine_table(
            homeserver.virtual_machines
        )

        container_table = render_container_table(
            homeserver.containers
        )

        network_table = render_network_table(
            homeserver.networks
        )

        zfs_table = render_zfs_table(
            homeserver.zfs_pools
        )

        zfs_warnings = render_zfs_warnings(
            homeserver.zfs_pools
        )

        disk_table = render_disk_table(
            homeserver.physical_disks
        )

        disk_warnings = render_disk_warnings(
            homeserver.physical_disks
        )

        docker_table = render_docker_table(
            homeserver.docker_containers
        )
        docker_stack_table = render_docker_stack_table(
            homeserver.docker_stacks
       )
        markdown = f"""# Homeserver

## Samenvatting

| Onderdeel | Waarde |
|---|---|
| Host | {host.hostname} |
| Proxmox | {host.proxmox_version} |
| Virtuele machines | {vm_count} |
| LXC-containers | {container_count} |
| Docker-containers | {docker_count} |
| Storage locaties | {storage_count} |
| ZFS-pools | {zfs_pool_count} |
| Fysieke disks | {physical_disk_count} |
| Netwerkinterfaces | {network_count} |
| Laatste inventarisatie | {inventory_time} |

## Waarschuwingen

### ZFS

{zfs_warnings}

### SMART

{disk_warnings}

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

## ZFS-status

{zfs_table}

## Fysieke disks / SMART

{disk_table}

## Virtuele machines

{vm_table}

## LXC-containers

{container_table}

## Docker Compose-stacks

{docker_stack_table}

## Docker-containers

{docker_table}

## Netwerk

{network_table}
"""

        target.write_text(
            markdown,
            encoding="utf-8",
        )

        return target
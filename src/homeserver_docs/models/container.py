"""LXC container models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Container:
    """A Proxmox LXC container."""

    vmid: int
    name: str
    status: str
    memory_mb: int | None = None
    swap_mb: int | None = None
    root_disk_gb: float | None = None
    cpu_cores: int | None = None
    network_interfaces: list[str] = field(default_factory=list)
    mountpoints: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    snapshots: list[str] = field(default_factory=list)
    backup_status: str | None = None
    startup_order: int | None = None
    description: str | None = None
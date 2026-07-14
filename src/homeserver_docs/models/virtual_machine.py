"""Virtual machine models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class VirtualDisk:
    """A disk attached to a virtual machine."""

    interface: str
    storage: str
    volume: str
    size_gb: float | None = None


@dataclass(frozen=True, slots=True)
class VirtualNetworkInterface:
    """A network interface attached to a virtual machine."""

    interface: str
    model: str
    bridge: str | None = None
    mac_address: str | None = None


@dataclass(frozen=True, slots=True)
class VirtualMachine:
    """A Proxmox virtual machine."""

    vmid: int
    name: str
    status: str
    cpu_cores: int
    memory_mb: int
    boot_disk_gb: float
    pid: int
    storage: list[str] = field(default_factory=list)
    disks: list[VirtualDisk] = field(default_factory=list)
    network_interfaces: list[VirtualNetworkInterface] = field(default_factory=list)
    ip_addresses: list[str] = field(default_factory=list)
    guest_os: str | None = None
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    snapshots: list[str] = field(default_factory=list)
    backup_status: str | None = None
    startup_order: int | None = None
    uptime: str | None = None
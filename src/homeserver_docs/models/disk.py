"""Physical disk models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PhysicalDisk:
    """A physical disk in the Proxmox host."""

    device: str
    model: str | None = None
    serial: str | None = None
    size: str | None = None
    smart_status: str | None = None
    temperature_c: int | None = None
    power_on_hours: int | None = None
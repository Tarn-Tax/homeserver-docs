"""Storage models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Storage:
    """A Proxmox storage location."""

    name: str
    storage_type: str
    status: str
    total_kib: int
    used_kib: int
    available_kib: int
    usage_percent: float
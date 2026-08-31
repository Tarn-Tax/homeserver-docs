"""Network models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NetworkInterface:
    """A Proxmox network interface or bridge."""

    name: str
    interface_type: str
    method: str
    address: str | None = None
    gateway: str | None = None
    bridge_ports: str | None = None
    comment: str | None = None
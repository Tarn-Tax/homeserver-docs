from dataclasses import dataclass


@dataclass(slots=True)
class Host:
    """Representation of a Proxmox host."""

    hostname: str
    proxmox_version: str
    kernel: str
    cpu_model: str
    cpu_cores: int
    memory_total: str
    uptime: str
"""Docker models."""

from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class DockerContainer:
    """A Docker container."""

    container_id: str
    name: str
    image: str
    state: str
    status: str
    health: str | None = None
    restart_policy: str | None = None
    ports: str | None = None
    networks: str | None = None
    compose_project: str | None = None
    compose_service: str | None = None
    compose_file: str | None = None
    mounts: list[str] = field(default_factory=list)
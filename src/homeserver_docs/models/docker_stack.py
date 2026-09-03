"""Docker Compose stack models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DockerStack:
    """A Docker Compose stack."""

    name: str
    compose_file: str | None = None
    containers: list[str] = field(default_factory=list)
    running_count: int = 0
    healthy_count: int = 0
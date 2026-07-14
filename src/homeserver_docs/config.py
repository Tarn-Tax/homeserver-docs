"""Application configuration."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ServerConfig:
    """Connection settings for a server."""

    host: str
    username: str
    port: int = 22


@dataclass(frozen=True, slots=True)
class OutputConfig:
    """Output settings."""

    directory: Path


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Complete application configuration."""

    proxmox: ServerConfig
    docker: ServerConfig
    homeassistant: ServerConfig
    output: OutputConfig


def load_config(path: Path = Path("homeserver.toml")) -> AppConfig:
    """Load application configuration from a TOML file."""

    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("rb") as config_file:
        data = tomllib.load(config_file)

    return AppConfig(
        proxmox=ServerConfig(**data["proxmox"]),
        docker=ServerConfig(**data["docker"]),
        homeassistant=ServerConfig(**data["homeassistant"]),
        output=OutputConfig(directory=Path(data["output"]["directory"])),
    )
"""Docker collector."""

from __future__ import annotations

import json
from dataclasses import replace

from homeserver_docs.config import load_config
from homeserver_docs.models.docker import DockerContainer
from homeserver_docs.parsers.docker import parse_docker_ps
from homeserver_docs.utils.ssh import SSHConnection


class DockerCollector:
    """Collect Docker containers from the Docker host."""

    def __init__(self, connection: SSHConnection | None = None) -> None:
        if connection is None:
            connection = SSHConnection(load_config().docker)

        self.connection = connection

    def collect(self) -> list[DockerContainer]:
        """Collect running Docker containers and mount information."""

        output = self.connection.run(
            "docker ps --format '{{json .}}'"
        )

        containers = parse_docker_ps(output)

        enriched: list[DockerContainer] = []

        for container in containers:
            mounts = self._collect_mounts(container.name)

            enriched.append(
                replace(
                    container,
                    mounts=mounts,
                )
            )

        return enriched

    def _collect_mounts(self, container_name: str) -> list[str]:
        """Collect mount source and destination for one container."""

        try:
            output = self.connection.run(
                "docker inspect "
                f"{container_name} "
                "--format='{{json .Mounts}}'"
            )
        except RuntimeError:
            return []

        try:
            items = json.loads(output)
        except json.JSONDecodeError:
            return []

        mounts: list[str] = []

        for item in items:
            source = item.get("Source")
            destination = item.get("Destination")
            mount_type = item.get("Type")

            if not source or not destination:
                continue

            mounts.append(
                f"{mount_type}: {source} → {destination}"
            )

        return mounts
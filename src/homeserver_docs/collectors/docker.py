"""Docker collector."""

from __future__ import annotations

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
        """Collect running Docker containers."""

        output = self.connection.run(
            "docker ps --format '{{json .}}'"
        )

        return parse_docker_ps(output)
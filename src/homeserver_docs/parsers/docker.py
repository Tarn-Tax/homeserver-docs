"""Docker parser."""

from __future__ import annotations

import json

from homeserver_docs.models.docker import DockerContainer


def parse_docker_ps(output: str) -> list[DockerContainer]:
    """Parse Docker ps JSON lines."""

    containers: list[DockerContainer] = []

    for line in output.splitlines():
        if not line.strip():
            continue

        data = json.loads(line)

        labels = _parse_labels(
            data.get("Labels", "")
        )

        containers.append(
            DockerContainer(
                container_id=data.get("ID", ""),
                name=data.get("Names", ""),
                image=data.get("Image", ""),
                state=data.get("State", ""),
                status=data.get("Status", ""),
                health=_optional(
                    data.get("HealthStatus")
                ),
                ports=_optional(
                    data.get("Ports")
                ),
                networks=_optional(
                    data.get("Networks")
                ),
                compose_project=labels.get(
                    "com.docker.compose.project"
                ),
                compose_service=labels.get(
                    "com.docker.compose.service"
                ),
                compose_file=labels.get(
                    "com.docker.compose.project.config_files"
                ),
            )
        )

    return containers


def _parse_labels(value: str) -> dict[str, str]:
    """Convert Docker label text to a dictionary."""

    labels: dict[str, str] = {}

    for item in value.split(","):
        if "=" not in item:
            continue

        key, label_value = item.split("=", 1)

        labels[key.strip()] = label_value.strip()

    return labels


def _optional(value: object | None) -> str | None:
    """Return None for empty Docker values."""

    if value is None:
        return None

    text = str(value).strip()

    if not text or text == "none":
        return None

    return text
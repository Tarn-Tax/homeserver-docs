"""Docker Compose stack service."""

from __future__ import annotations

from collections import defaultdict

from homeserver_docs.models.docker import DockerContainer
from homeserver_docs.models.docker_stack import DockerStack


def build_docker_stacks(
    containers: list[DockerContainer],
) -> list[DockerStack]:
    """Group Docker containers by Compose project."""

    grouped: dict[str, list[DockerContainer]] = defaultdict(list)

    for container in containers:
        if not container.compose_project:
            continue

        grouped[container.compose_project].append(container)

    stacks: list[DockerStack] = []

    for name, stack_containers in sorted(grouped.items()):
        compose_file = next(
            (
                container.compose_file
                for container in stack_containers
                if container.compose_file
            ),
            None,
        )

        running_count = sum(
            container.state == "running"
            for container in stack_containers
        )

        healthy_count = sum(
            container.health == "healthy"
            for container in stack_containers
        )

        stacks.append(
            DockerStack(
                name=name,
                compose_file=compose_file,
                containers=[
                    container.name
                    for container in stack_containers
                ],
                running_count=running_count,
                healthy_count=healthy_count,
            )
        )

    return stacks
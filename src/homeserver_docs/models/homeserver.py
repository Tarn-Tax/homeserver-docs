"""Homeserver model."""

from __future__ import annotations

from dataclasses import dataclass, field

from homeserver_docs.models.container import Container
from homeserver_docs.models.disk import PhysicalDisk
from homeserver_docs.models.docker import DockerContainer
from homeserver_docs.models.host import Host
from homeserver_docs.models.network import NetworkInterface
from homeserver_docs.models.storage import Storage
from homeserver_docs.models.virtual_machine import VirtualMachine
from homeserver_docs.models.zfs import ZfsPool


@dataclass(slots=True)
class Homeserver:
    """Complete inventory of a homeserver environment."""

    host: Host
    storage: list[Storage] = field(default_factory=list)
    virtual_machines: list[VirtualMachine] = field(default_factory=list)
    containers: list[Container] = field(default_factory=list)
    docker_containers: list[DockerContainer] = field(default_factory=list)
    networks: list[NetworkInterface] = field(default_factory=list)
    zfs_pools: list[ZfsPool] = field(default_factory=list)
    physical_disks: list[PhysicalDisk] = field(default_factory=list)
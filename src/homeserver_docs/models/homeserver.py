"""Homeserver model."""

from __future__ import annotations

from dataclasses import dataclass, field

from homeserver_docs.models.container import Container
from homeserver_docs.models.host import Host
from homeserver_docs.models.network import NetworkInterface
from homeserver_docs.models.storage import Storage
from homeserver_docs.models.virtual_machine import VirtualMachine


@dataclass(slots=True)
class Homeserver:
    """Complete inventory of a homeserver environment."""

    host: Host
    storage: list[Storage] = field(default_factory=list)
    virtual_machines: list[VirtualMachine] = field(default_factory=list)
    containers: list[Container] = field(default_factory=list)
    networks: list[NetworkInterface] = field(default_factory=list)
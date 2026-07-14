"""Inventory service."""

from __future__ import annotations

from homeserver_docs.collectors.host import HostCollector
from homeserver_docs.collectors.storage import StorageCollector
from homeserver_docs.collectors.virtual_machine import VirtualMachineCollector
from homeserver_docs.models.homeserver import Homeserver


class InventoryService:
    """Coordinate all collectors."""

    def __init__(self) -> None:
        self.host_collector = HostCollector()
        self.storage_collector = StorageCollector()
        self.virtual_machine_collector = VirtualMachineCollector()

    def collect(self) -> Homeserver:
        """Collect the complete homeserver inventory."""

        return Homeserver(
            host=self.host_collector.collect(),
            storage=self.storage_collector.collect(),
            virtual_machines=self.virtual_machine_collector.collect(),
        )
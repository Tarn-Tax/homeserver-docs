"""Inventory service."""

from __future__ import annotations

from homeserver_docs.collectors.container import ContainerCollector
from homeserver_docs.collectors.disk import DiskCollector
from homeserver_docs.collectors.host import HostCollector
from homeserver_docs.collectors.network import NetworkCollector
from homeserver_docs.collectors.storage import StorageCollector
from homeserver_docs.collectors.virtual_machine import VirtualMachineCollector
from homeserver_docs.collectors.zfs import ZfsCollector
from homeserver_docs.models.homeserver import Homeserver


class InventoryService:
    """Coordinate all collectors."""

    def __init__(self) -> None:
        self.host_collector = HostCollector()
        self.storage_collector = StorageCollector()
        self.virtual_machine_collector = VirtualMachineCollector()
        self.container_collector = ContainerCollector()
        self.network_collector = NetworkCollector()
        self.zfs_collector = ZfsCollector()
        self.disk_collector = DiskCollector()

    def collect(self) -> Homeserver:
        """Collect the complete homeserver inventory."""

        return Homeserver(
            host=self.host_collector.collect(),
            storage=self.storage_collector.collect(),
            virtual_machines=self.virtual_machine_collector.collect(),
            containers=self.container_collector.collect(),
            networks=self.network_collector.collect(),
            zfs_pools=self.zfs_collector.collect(),
            physical_disks=self.disk_collector.collect(),
        )
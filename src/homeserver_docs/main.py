"""
Homeserver Documentation Framework.

Main application.
"""

from __future__ import annotations

import logging
from pathlib import Path

from homeserver_docs.collectors.host import HostCollector
from homeserver_docs.collectors.storage import StorageCollector
from homeserver_docs.collectors.virtual_machine import VirtualMachineCollector
from homeserver_docs.renderers.markdown import MarkdownRenderer
from homeserver_docs.services.inventory import InventoryService


def configure_logging() -> None:
    """Configure application logging."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )


def main(mode: str = "full") -> int:
    """Run the requested inventory mode."""

    configure_logging()

    logging.info("Homeserver Documentation Framework")

    if mode == "host":
        print(HostCollector().collect())
        return 0

    if mode == "storage":
        for storage in StorageCollector().collect():
            print(storage)
        return 0

    if mode == "vm":
        for virtual_machine in VirtualMachineCollector().collect():
            print(virtual_machine)
        return 0

    if mode == "full":
        logging.info("Starting inventory...")

        homeserver = InventoryService().collect()
        output_file = MarkdownRenderer().render(
            homeserver,
            Path("output"),
        )

        logging.info("Generated: %s", output_file)
        return 0

    raise ValueError(f"Onbekende inventarisatiemodus: {mode}")
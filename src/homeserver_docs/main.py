"""
Homeserver Documentation Framework.

Main application.
"""

from __future__ import annotations

import logging
from pathlib import Path

from homeserver_docs.collectors.host import HostCollector
from homeserver_docs.renderers.markdown import MarkdownRenderer


def configure_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )


def main() -> int:
    """Application entry point."""

    configure_logging()

    logging.info("Homeserver Documentation Framework")
    logging.info("Starting inventory...")

    host = HostCollector().collect()

    renderer = MarkdownRenderer()
    output_file = renderer.render_host(
        host,
        Path("output"),
    )

    logging.info("Generated: %s", output_file)

    return 0
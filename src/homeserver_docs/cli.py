"""Command line interface."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        prog="homeserver-docs",
        description="Homeserver Documentation Framework",
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="full",
        choices=[
            "full",
            "host",
            "storage",
            "vm",
        ],
        help="Inventory mode",
    )

    return parser.parse_args()
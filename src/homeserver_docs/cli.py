"""Command-line interface."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="homeserver-docs",
        description="Inventariseer en documenteer de homeserver.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
    )

    subparsers.add_parser(
        "full",
        help="Voer de volledige inventarisatie uit.",
    )
    subparsers.add_parser(
        "host",
        help="Toon alleen de Proxmox-host.",
    )
    subparsers.add_parser(
        "storage",
        help="Toon alleen Proxmox-storage.",
    )
    subparsers.add_parser(
        "vm",
        help="Toon alleen virtuele machines.",
    )

    return parser


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = build_parser()
    arguments = parser.parse_args()

    if arguments.command is None:
        arguments.command = "full"

    return arguments
"""QEMU guest network parser."""

from __future__ import annotations

import ipaddress
import json


def parse_guest_ipv4_addresses(output: str) -> list[str]:
    """Extract useful IPv4 addresses from QEMU Guest Agent output."""

    data = json.loads(output)

    addresses: list[str] = []

    for interface in data:
        for address in interface.get("ip-addresses", []):
            if address.get("ip-address-type") != "ipv4":
                continue

            ip = address.get("ip-address")

            if not ip:
                continue

            parsed = ipaddress.ip_address(ip)

            if parsed.is_loopback:
                continue

            if ip.startswith("172.30."):
                continue

            addresses.append(ip)

    return addresses
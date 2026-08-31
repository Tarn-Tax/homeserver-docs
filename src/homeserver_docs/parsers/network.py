"""Proxmox network configuration parser."""

from __future__ import annotations

from homeserver_docs.models.network import NetworkInterface


def parse_network_interfaces(output: str) -> list[NetworkInterface]:
    """Parse /etc/network/interfaces."""

    interfaces: list[NetworkInterface] = []
    lines = output.splitlines()

    current: dict[str, str] | None = None

    def save_current() -> None:
        nonlocal current

        if current is None:
            return

        name = current["name"]

        interfaces.append(
            NetworkInterface(
                name=name,
                interface_type=(
                    "bridge" if name.startswith("vmbr") else "physical"
                ),
                method=current.get("method", "unknown"),
                address=current.get("address"),
                gateway=current.get("gateway"),
                bridge_ports=current.get("bridge-ports"),
                comment=current.get("comment"),
            )
        )

        current = None

    for raw_line in lines:
        line = raw_line.strip()

        if line.startswith("iface "):
            save_current()

            parts = line.split()

            if len(parts) >= 4:
                current = {
                    "name": parts[1],
                    "method": parts[3],
                }

            continue

        if current is None:
            continue

        if line.startswith("#"):
            current["comment"] = line[1:].strip()
            continue

        for key in ("address", "gateway", "bridge-ports"):
            if line.startswith(f"{key} "):
                current[key] = line.split(None, 1)[1]
                break

    save_current()

    return interfaces
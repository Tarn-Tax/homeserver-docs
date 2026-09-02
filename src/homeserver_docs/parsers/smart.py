"""SMART information parser."""

from __future__ import annotations

import re


def parse_smart_info(output: str) -> dict[str, object]:
    """Parse useful information from SATA or NVMe smartctl output."""

    result: dict[str, object] = {
        "smart_status": None,
        "temperature_c": None,
        "power_on_hours": None,
    }

    health_match = re.search(
        r"SMART overall-health self-assessment test result:\s*(.+)",
        output,
    )

    if health_match:
        result["smart_status"] = health_match.group(1).strip()

    # SATA temperature
    temperature_match = re.search(
        r"^\s*194\s+Temperature_Celsius.*?\s(\d+)(?:\s+\(|$)",
        output,
        re.MULTILINE,
    )

    # NVMe temperature
    if not temperature_match:
        temperature_match = re.search(
            r"^Temperature:\s+(\d+)\s+Celsius",
            output,
            re.MULTILINE,
        )

    if temperature_match:
        result["temperature_c"] = int(
            temperature_match.group(1)
        )

    # SATA power-on hours
    hours_match = re.search(
        r"^\s*9\s+Power_On_Hours.*?\s(\d+)\s*$",
        output,
        re.MULTILINE,
    )

    # NVMe power-on hours
    if not hours_match:
        hours_match = re.search(
            r"^Power On Hours:\s+([\d,]+)",
            output,
            re.MULTILINE,
        )

    if hours_match:
        result["power_on_hours"] = int(
            hours_match.group(1).replace(",", "")
        )

    return result
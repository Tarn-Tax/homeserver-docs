"""
Command execution utilities.
"""

from __future__ import annotations

import subprocess


class CommandRunner:
    """Execute operating system commands."""

    def run(self, command: list[str]) -> str:
        """Execute a command and return stdout."""

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed ({result.returncode}): "
                f"{' '.join(command)}\n"
                f"{result.stderr.strip()}"
            )

        return result.stdout.strip()
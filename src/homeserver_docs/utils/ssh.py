"""SSH connection utilities."""

from __future__ import annotations

import subprocess

from homeserver_docs.config import ServerConfig


class SSHConnection:
    """Execute commands on a remote server over SSH."""

    def __init__(self, config: ServerConfig) -> None:
        self.config = config

    def run(self, command: str) -> str:
        """Execute a command over SSH and return stdout."""

        ssh_command = [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=10",
            "-o",
            "ServerAliveInterval=5",
            "-p",
            str(self.config.port),
            f"{self.config.username}@{self.config.host}",
            command,
        ]

        try:
            result = subprocess.run(
                ssh_command,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                f"SSH-opdracht duurde langer dan 20 seconden: {command}"
            ) from error

        if result.returncode != 0:
            raise RuntimeError(
                f"SSH-opdracht mislukt ({result.returncode}): {command}\n"
                f"{result.stderr.strip()}"
            )

        return result.stdout.strip()
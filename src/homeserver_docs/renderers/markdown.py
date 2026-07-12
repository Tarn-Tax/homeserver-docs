"""
Markdown renderers.
"""

from __future__ import annotations

from pathlib import Path

from homeserver_docs.models.host import Host


class MarkdownRenderer:
    """Render collected data as Markdown."""

    def render_host(self, host: Host, output_dir: Path) -> Path:
        """
        Render host information to Markdown.

        Returns the generated file path.
        """

        output_dir.mkdir(parents=True, exist_ok=True)

        target = output_dir / "01-host.md"

        target.write_text(
            f"""# Proxmox Host

## Hostname

{host.hostname}

## Proxmox Version

{host.proxmox_version}

## Kernel

{host.kernel}
""",
            encoding="utf-8",
        )

        return target
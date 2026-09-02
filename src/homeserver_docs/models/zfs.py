"""ZFS models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ZfsDevice:
    """A device belonging to a ZFS pool."""

    name: str
    state: str
    read_errors: int = 0
    write_errors: int = 0
    checksum_errors: int = 0


@dataclass(frozen=True, slots=True)
class ZfsPool:
    """Status of a ZFS pool."""

    name: str
    state: str
    status_message: str | None = None
    data_errors: str | None = None
    devices: list[ZfsDevice] = field(default_factory=list)

    @property
    def healthy(self) -> bool:
        """Return whether the pool has no detected problems."""

        return (
            self.state == "ONLINE"
            and not self.status_message
            and all(
                device.read_errors == 0
                and device.write_errors == 0
                and device.checksum_errors == 0
                for device in self.devices
            )
        )
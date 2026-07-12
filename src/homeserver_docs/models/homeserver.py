from dataclasses import dataclass, field

from homeserver_docs.models.host import Host


@dataclass(slots=True)
class Homeserver:
    """Complete inventory of a homeserver environment."""

    host: Host
    storage: list[object] = field(default_factory=list)
    networks: list[object] = field(default_factory=list)
    virtual_machines: list[object] = field(default_factory=list)
    containers: list[object] = field(default_factory=list)
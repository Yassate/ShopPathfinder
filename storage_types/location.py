from dataclasses import dataclass, field

@dataclass(frozen=True)
class Location:
    x: int = field(compare=True)
    y: int = field(compare=True)
    name: str = field(compare=False, default_factory=lambda: "viaPoint")


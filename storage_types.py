from dataclasses import dataclass, field


@dataclass(frozen=True)
class Location:
    x: int = field(compare=True)
    y: int = field(compare=True)
    name: str = field(compare=False, default_factory=lambda: "viaPoint")


@dataclass
class Path:
    locations: list[Location]

    def length(self) -> int:
        return len(self.locations)

    def is_between_points(self, loc1: Location, loc2: Location) -> bool:
        pos_start = self.locations[0]
        pos_end = self.locations[-1]
        return ((pos_start == loc1 and pos_end == loc2) or (pos_start == loc2 and pos_end == loc1))

from dataclasses import dataclass

@dataclass
class Location:
    x: int
    y: int
    name: str = "viaPoint"

@dataclass
class Path:
    positions: list[Location]

    def is_between_points(self, pt1, pt2):
        pos_start = self.positions[0]
        pos_end = self.positions[-1]
        return ((pos_start == pt1 and pos_end == pt2) or (pos_start == pt2 and pos_end == pt1))

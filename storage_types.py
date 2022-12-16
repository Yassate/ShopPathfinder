from dataclasses import dataclass

@dataclass
class Location:
    x: int
    y: int
    name: str = "viaPoint"

@dataclass
class Path:
    positions: list[Location]   

    def set_start_loc(self, start_loc: Location):
        self.positions[0] = start_loc

    def set_target_loc(self, target_loc: Location):
        self.positions[-1] = target_loc

    def is_between_points(self, pt1, pt2):
        pos_start = self.positions[0]
        pos_end = self.positions[-1]
        print(f"Pt1: {pt1}, Pt2: {pt2}, Pos start: {pos_start}, pos end: {pos_end}")
        return ((pos_start == pt1 and pos_end == pt2) or (pos_start == pt2 and pos_end == pt1))

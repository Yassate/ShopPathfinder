from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

@dataclass
class City(Position):
    name: str = "RandomCity"

@dataclass
class Path:
    positions: list[Position]
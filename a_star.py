import numpy as np
import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from storage_types import Location, Path
from colors import LGREY, DGREY, GREEN, RED


class AreaGrid:
    _color = [DGREY, LGREY, GREEN, RED]

    def __init__(self, filepath: str = "", wh_pix: tuple[int, int] = (500, 500), cover: int = 1, spacing: int = 1):
        self._grid = self._load_data_from_file(filepath)
        self._org_grid = self._grid.copy()
        self.shape = self._grid.shape
        self.cover = cover
        self.spacing = spacing
        self.el_w_pix = np.floor(wh_pix[0]*self.cover/self.shape[0])-self.spacing
        self.el_h_pix = np.floor(wh_pix[1]*self.cover/self.shape[1])-self.spacing
        self._path: Path
        self._cached_paths: list[Path] = []

    def _load_data_from_file(self, filepath: str) -> np.ndarray:
        loaded = np.genfromtxt(filepath, delimiter=" ", dtype=np.int8, filling_values=1)
        loaded[loaded == 0] = 90
        return loaded

    def _check_for_cached_solution(self, loc1: Location, loc2: Location) -> Path:
        for path in self._cached_paths:
            if path.is_between_points(loc1, loc2):
                return path

    def set_path(self, path: Path):
        self._path = path
        for location in path.locations[1:-1]:
            self._grid.itemset((location.y, location.x), -2)

    def set_location(self, location: Location):
        self._grid.itemset((location.y, location.x), 3)

    def reset_location(self, location: Location):
        val = self._org_grid.item((location.y, location.x))
        self._grid.itemset((location.y, location.x), val)

    def reset_grid(self):
        self._grid = self._org_grid.copy()

    def draw(self, WIN: pygame.Surface):
        for y, col in enumerate(self._grid):
            for x, row in enumerate(col):
                color = DGREY if row == 90 else self._color[abs(row)]
                pygame.draw.rect(WIN, color, pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))

    def solve_for_locations(self, start_loc: Location, target_loc: Location) -> Path:
        if cached_path:= self._check_for_cached_solution(start_loc, target_loc):
            return cached_path
        else:
            grid = Grid(matrix=self._org_grid)
            start = grid.node(start_loc.x, start_loc.y)
            end = grid.node(target_loc.x, target_loc.y)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, _ = finder.find_path(start, end, grid)
            cur_path = Path([start_loc] + [Location(p[0], p[1]) for p in path[1:-1]] + [target_loc])
            self._cached_paths.append(cur_path)
            return cur_path

    def get_shortest_length_between_locations(self, loc1: Location, loc2: Location) -> int:
        path = self.solve_for_locations(loc1, loc2)
        return path.length()

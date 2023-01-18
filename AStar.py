import numpy as np
import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from storage_types import Location, Path

class AreaGrid:
    RED   = (255, 30, 70)
    BLACK = (0, 0, 0)
    GREEN = (0, 168, 107)
    WHITE = (255, 255, 255)
    LGRAY = (180, 180, 180)
    GRAY  = (128, 128, 128)
    DGRAY = (100, 100, 100)
    _color = [DGRAY, LGRAY, GREEN, RED]

    def __init__(self, win, filepath="", wh_pix=(500, 500), cover=1, spacing=1):
        self._window = win
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
        return np.genfromtxt(filepath, delimiter=" ", dtype=np.int8, filling_values=1)

    def reset_grid(self):
        self._grid = self._org_grid.copy()

    def draw(self):
        for y, col in enumerate(self._grid):
            for x, row in enumerate(col):
                pygame.draw.rect(self._window, self._color[abs(row)], pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))    

    def set_path(self, path):
        self._path = path
        for location in path.locations:
            self._grid.itemset((location.y, location.x), -2)

    def check_for_cached_solution(self, pt1, pt2):
        for path in self._cached_paths:
            if path.is_between_points(pt1, pt2):
                # print("Found in cache\n\n")
                return path

    def set_location(self, location):
        self._grid.itemset((location.y, location.x), -3)

    def solve_for_locations(self, pt1, pt2):
        if cached_path:= self.check_for_cached_solution(pt1, pt2):
            cur_path = cached_path
        else:
            grid = Grid(matrix=self._grid)
            start = grid.node(pt1.x, pt1.y)
            end = grid.node(pt2.x, pt2.y)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, _ = finder.find_path(start, end, grid)
            cur_path = Path([Location(p[0], p[1]) for p in path])
            cur_path.set_start_loc(pt1)
            cur_path.set_target_loc(pt2)
            self._cached_paths.append(cur_path)
        self.set_path(cur_path)

    def get_shortest_length_between_locations(self, pt1, pt2) -> int:
        self.solve_for_locations(pt1, pt2)
        return self._path.length()

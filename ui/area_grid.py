import numpy as np
import pygame
from storage_types import Location, Path
from ui.colors import LGREY, DGREY, GREEN, RED


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

    def _load_data_from_file(self, filepath: str) -> np.ndarray:
        loaded = np.genfromtxt(filepath, delimiter=" ", dtype=np.int8, filling_values=1)
        loaded[loaded == 0] = 90
        return loaded

    def set_path(self, path: Path):
        self._path = path
        for location in path.locations[1:-1]:
            self._grid.itemset((location.y, location.x), -2)

    def set_location(self, location: Location):
        self._grid.itemset((location.y, location.x), 3)

    def reset_location(self, location: Location):
        val = self._org_grid.item((location.y, location.x))
        self._grid.itemset((location.y, location.x), val)

    def reset(self):
        self._grid = self._org_grid.copy()

    def get_org_grid(self):
        return self._org_grid.copy()

    def draw(self, WIN: pygame.Surface):
        for y, col in enumerate(self._grid):
            for x, row in enumerate(col):
                color = DGREY if row == 90 else self._color[abs(row)]
                pygame.draw.rect(WIN, color, pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))

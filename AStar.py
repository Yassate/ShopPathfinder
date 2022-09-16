import numpy as np
import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#TODO Purpose of this class -> to be a service that gives you back a path between the points. No more probably

def generate_obstacles(gridsize, obstacle_size=(30, 80), count=3):
    internal_grid = np.ones((gridsize,gridsize), dtype=np.int8)
    for i in range(count):
        start_x = random.randint(max(obstacle_size), gridsize-max(obstacle_size)-1)
        start_y = random.randint(max(obstacle_size), gridsize-max(obstacle_size)-1)
        size_x = obstacle_size[(x_i:=random.randint(0,1))]
        size_y = obstacle_size[abs(x_i-1)]
        internal_grid[start_x:start_x+size_x, start_y:start_y+size_y] = 0
    return internal_grid

class AreaGrid:
    RED   = (255, 30, 70)
    BLACK = (0, 0, 0)
    GREEN = (0, 168, 107)
    WHITE = (255, 255, 255)
    LGRAY = (180, 180, 180)
    GRAY  = (128, 128, 128)
    DGRAY = (100, 100, 100)
    _color = [DGRAY, LGRAY, GREEN] 

    def __init__(self, win=[], size=10, wh_pix=(500, 500),cover=1, spacing=1):
        self._window = win
        self.size = size
        self.reset_grid()
        self.w_pix = wh_pix[0]
        self.h_pix = wh_pix[1]
        self.el_w_pix = np.floor(self.w_pix*cover/size)-spacing
        self.el_h_pix = np.floor(self.h_pix*cover/size)-spacing
        self.spacing=spacing
        self._path = []

    def reset_grid(self):
        self._grid = np.ones((self.size, self.size), dtype=np.int8)

    def set_start(self, start):
        self._start = start
        self._grid.itemset(start, 2)

    def set_end(self, end):
        self._end = end
        self._grid.itemset(end, 2)

    def add_obstacles_from_grid(self, obst_grid):
        self._grid = np.multiply(self._grid, obst_grid)

    def draw(self):
        for y, col in enumerate(self._grid):
            for x, row in enumerate(col):
                pygame.draw.rect(self._window, self._color[abs(row)], pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))    

    def set_path(self, path):
        for step in path:
            self._path.append(row_col_step:=step[::-1])
            self._grid.itemset(row_col_step, -2)

    def solve_path(self):
        grid = Grid(matrix=self._grid)
        start = grid.node(*self._start[::-1])
        end = grid.node(*self._end[::-1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        self.set_path(path)

    def get_solution(self):
        grid = Grid(matrix=self._grid)
        start = grid.node(*self._start[::-1])
        end = grid.node(*self._end[::-1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        return path

    def get_solution_from_positions(self, pt1, pt2):
        self._start = (pt1.x, pt1.y)
        self._end = (pt2.x, pt2.y)
        return self.get_solution()

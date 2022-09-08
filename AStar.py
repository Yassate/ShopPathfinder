import numpy as np
import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def generate_obstacles(gridsize, obstacle_size=(30, 80)):
    internal_grid = np.ones((gridsize,gridsize), dtype=np.int8)
    for i in range(3):
        start_x = random.randint(max(obstacle_size), gridsize-max(obstacle_size)-1)
        start_y = random.randint(max(obstacle_size), gridsize-max(obstacle_size)-1)
        size_x = obstacle_size[(x_i:=random.randint(0,1))]
        size_y = obstacle_size[abs(x_i-1)]
        internal_grid[start_x:start_x+size_x, start_y:start_y+size_y] = 0
    return internal_grid

class AreaGrid:
    RED = (255, 30, 70)
    BLACK = (0, 0, 0)
    GREEN = (0,168,107)
    _color = [BLACK, RED, GREEN] 

    def __init__(self, win=[], size=10, wh_pix=(500, 500), obstacles=[], cover=0.9, spacing=1):
        self._win = win
        self._grid = np.ones((size,size), dtype=np.int8)
        self._obstacles = obstacles
        self.add_obstacles()
        self.size = size
        self.w_pix = wh_pix[0]
        self.h_pix = wh_pix[1]
        self.obstacles = obstacles
        self.el_w_pix = np.floor(self.w_pix*cover/size)-spacing
        self.el_h_pix = np.floor(self.h_pix*cover/size)-spacing
        self.spacing=spacing

    def set_start(self, start):
        self._start = start
        self._grid.itemset(start, 2)

    def set_end(self, end):
        self._end = end
        self._grid.itemset(end, 2)

    def add_obstacles(self):
        for obstacle in self._obstacles:
            self._grid.itemset(obstacle, 0)

    def add_obstacles_from_grid(self, obst_grid):
        # TODO LOOKS like it's working, but pathplanner ignores some of grid 0 elements
        self._grid = np.multiply(self._grid, obst_grid)


    def print_grid(self):
        print(type(self._grid))
        print(self._grid)

    def draw(self):
        # for x, col in enumerate(self._grid):
        #     for y, row in enumerate(col):
        #         pygame.draw.rect(self._win, self._color[abs(row)], pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))    
        #         #pygame.display.update()
        for y, col in enumerate(self._grid):
            for x, row in enumerate(col):
                pygame.draw.rect(self._win, self._color[abs(row)], pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))    
                #pygame.display.update()

    def add_path(self, path):
        #self.print_grid()
        for step in path:
            self._grid.itemset((step[1], step[0]), -2)
        #self.print_grid()


    def solve_path(self):
        grid = Grid(matrix=self._grid)
        start = grid.node(*self._start)
        end = grid.node(*self._end)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        print(grid.grid_str())
        self.add_path(path)
        print(grid.grid_str())


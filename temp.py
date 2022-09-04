from xml.dom.minidom import parseString
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pygame
import numpy as np

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=RED, center=city, radius=5)

class AreaGrid:
    def __init__(self, size=10, wh_pix=(500, 500), obstacles=[], cover=0.9, spacing=1):
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
        self._color = [BLACK, RED, GREEN]


    def set_start(self, start):
        self._start = start
        self._grid.itemset(start, -2)

    def set_end(self, end):
        self._end = end
        self._grid.itemset(end, 2)

    def add_obstacles(self):
        for obstacle in self._obstacles:
            self._grid.itemset(obstacle, 0)
    

    def draw(self):
        for x, col in enumerate(self._grid):
            for y, row in enumerate(col):
                pygame.draw.rect(WIN, self._color[abs(row)], pygame.Rect(x*(self.el_w_pix+self.spacing), y*(self.el_h_pix+self.spacing), self.el_w_pix, self.el_h_pix))    
                #pygame.display.update()

    def add_path(self, path):
        for step in path:
            self._grid.itemset(step, -2)

    def solve_path(self):
        grid = Grid(matrix=self._grid)
        start = grid.node(*self._start)
        end = grid.node(*self._end)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        print(path)
        self.add_path(path)

def draw_window():
    WIN.fill(WHITE)
    mygrid.draw()
    pygame.display.update()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
RED = (255, 30, 70)
BLACK = (0, 0, 0)
GREEN = (0,168,107)
FPS = 60
cities_count = 2
cities = []

gridsize = 10

mygrid = AreaGrid(gridsize, (WIDTH, HEIGHT), obstacles=[(5,5), (5,6), (5,7), (6,5), (7,5)])
mygrid.set_start((1,1))
mygrid.set_end((6,6))

def main():
    clock = pygame.time.Clock()
    run = True
    draw_window()
    pygame.time.wait(2000)
    mygrid.solve_path()
    draw_window()

    while run:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    

    pygame.quit()

if __name__ == "__main__":
    main()
















matrix = [
  [1, 1, 1, 1],
  [1, 0, 1, 1],
  [1, 1, 1, 1]
]
grid = Grid(matrix=matrix)
start = grid.node(0, 0)
end = grid.node(3, 2)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)
#path=list of x,y tuples where travel should occur (closest path)
print(path)


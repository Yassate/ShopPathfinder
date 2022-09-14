from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid, generate_obstacles

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=(255,0,0), center=city, radius=5)

def draw_window(mygrid):
    WIN.fill(LGRAY)
    mygrid.draw()
    pygame.display.update()

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
LGRAY = (180, 180, 180)
FPS = 60

cities_count = 2
cities = []
gridsize = 200

def main():
    mygrid = AreaGrid(win=WIN, size=gridsize, wh_pix=(WIDTH, HEIGHT))
    obstacles = generate_obstacles(gridsize, obstacle_size=(round(gridsize/15),round(gridsize/8)), count=(min(40, gridsize)))
    mygrid.add_obstacles_from_grid(obstacles)
    mygrid.set_start((round(gridsize/10), round(gridsize/10)))
    mygrid.set_end((round(gridsize*9/10), round(gridsize*9/10)))


    clock = pygame.time.Clock()
    run = True
    draw_window(mygrid)
    pygame.time.wait(2000)
    mygrid.solve_path()
    draw_window(mygrid)

    while run:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    

    pygame.quit()

if __name__ == "__main__":
    main()
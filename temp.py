from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid, generate_obstacles

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=(255,0,0), center=city, radius=5)

def draw_window(mygrid):
    WIN.fill(WHITE)
    mygrid.draw()
    pygame.display.update()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)

FPS = 60
cities_count = 2
cities = []

gridsize = 10


def main():
    mygrid = AreaGrid(win=WIN, size=gridsize, wh_pix=(WIDTH, HEIGHT), obstacles=[(5,5), (5,6), (5,7), (5,8), (6,5), (7,5), (8,5)])
    mygrid.add_obstacles_from_grid(generate_obstacles(gridsize, obstacle_size=(1,3)))
    mygrid.set_start((1,2))
    mygrid.set_end((6,7))


    clock = pygame.time.Clock()
    run = True
    #mygrid.print_grid()
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
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=(255,0,0), center=city, radius=5)

def draw_window():
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

mygrid = AreaGrid(win=WIN, size=gridsize, wh_pix=(WIDTH, HEIGHT), obstacles=[(5,5), (5,6), (5,7), (6,5), (7,5)])
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
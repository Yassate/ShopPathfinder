from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
import random
from AStar import AreaGrid
from storage_types import Position, City, Path

def draw_cities(cities):
    for city in cities:
        pygame.draw.circle(surface=WIN, color=(255,0,0), center=city, radius=5)

def draw_window(mygrid):
    WIN.fill(LGRAY)
    mygrid.draw()
    pygame.display.update()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
LGRAY = (180, 180, 180)
FPS = 30
CITIES_COUNT = 10


def main():
    clock = pygame.time.Clock()
    run = True

    mygrid = AreaGrid(win=WIN, filepath="input_files/obstacles.txt", wh_pix=(WIDTH, HEIGHT))
    gridsize = mygrid.shape[0]

    #TODO STEP1 - Generate random cities as list of tuples or dataclasses - DONE
    #TODO STEP2 - Cities should be located somewhere on the borders - DONE
    #TODO STEP3 - Feed AStar solver with city pairs, keep results for each pair anyhow - DONE, kept in "_cached_paths" in AStar
    #TODO STEP4 - Round-robin every city pair and save results - DONE, as above
    #TODO STEP5 - Create shop-like map; with long shop shelves - DONE, loaded from file
    #TODO STEP5.5 A* doesn't work anymore, fix it
    #TODO STEP6 - Better algorithm for generating city coordinates, it should check coordinates if they are not taken by obstacle
    #TODO STEP7 - find a way for searching in the list for the path between given cities; it should be our distance calculation function
    #TODO STEP8 - perform traveling salesman on list of cities using distance calculation from STEP3
    #TODO STEP9 - draw everything

    cities = []

    for i in range(int(CITIES_COUNT/2)):
        pos_range = int(gridsize*0.05), int(gridsize*0.98)
        l_pos = int(gridsize*0.02), random.randint(*pos_range)
        r_pos = int(gridsize*0.95), random.randint(*pos_range)
        cities.append(City(Position(*l_pos)))
        cities.append(City(Position(*r_pos)))

    i=0
    j=1
    k=0

    while run:
        clock.tick(FPS)
        st = time.time()
        #mygrid.solve_for_positions(cities[i].position, cities[j].position)
        ex_time = time.time() - st
        dt = time.time()
        draw_window(mygrid)
        print(f"Drawing took {time.time()-dt} seconds")
        print(f"Solution for city pair no {i}, between city {i} and {j} found in {ex_time} seconds")
        pygame.time.wait(100)

        if j==CITIES_COUNT-1:
            i += 1
            j = i
        j += 1

        if i==CITIES_COUNT-2:
            k += 1
            i = 0
        if k==5:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
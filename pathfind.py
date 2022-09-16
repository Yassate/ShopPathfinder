from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
from AStar import AreaGrid, generate_obstacles
from storage_types import Position, City, Path

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
FPS = 30

cities_count = 10
gridsize = 200

def main():
    clock = pygame.time.Clock()
    run = True

    mygrid = AreaGrid(win=WIN, size=gridsize, wh_pix=(WIDTH, HEIGHT))
    obstacles = generate_obstacles(gridsize, obstacle_size=(round(gridsize/15),round(gridsize/8)), count=(min(40, gridsize)))



    #TODO STEP1 - Generate random cities as list of tuples or dataclasses - DONE
    #TODO STEP1.1 - Cities should be located somewhere on the borders, maybe 5 with fixed low X value and 5 with fixed high X value
    #TODO STEP2 - Feed AStar solver with city pairs (round-robin), result for each pair 
    #             should be dataclass "Path", with 2 cities inside and path as a list of tuples; store paths in list
    #TODO STEP3 - find a way for searching in the list for the path between given cities; it should be our distance calculation function
    #TODO STEP4 - perform traveling salesman on list of cities using distance calculation from STEP3
    #TODO STEP5 - draw evertything

    cities = []

    for i in range(int(cities_count/2)):
        cities.append(City(int(gridsize*0.05), random.randint(1, gridsize)))
    for j in range(int(cities_count/2)):
        cities.append(City(int(gridsize*0.95), random.randint(1, gridsize)))

    print(cities)
    i=1

    while run:
        clock.tick(FPS)

        mygrid.reset_grid()
        mygrid.add_obstacles_from_grid(obstacles)
        print(i)
        mygrid.set_start((cities[i].x, cities[i].y))
        mygrid.set_end((cities[i+1].x, cities[i+1].y))
        draw_window(mygrid)
        mygrid.solve_path()
        draw_window(mygrid)
        pygame.time.wait(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        i += 1
        if i==cities_count-2:
            break

    pygame.quit()

if __name__ == "__main__":
    main()
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
import pygame
from AStar import AreaGrid
from storage_types import Location

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
    #TODO STEP5.5 A* doesn't work anymore, fix it - DONE
    #TODO STEP6 - Generate smth around 10 of cities (anyway, it should be renamed to locations or products) - DONE
    #TODO STEP6.5 - move them to main? or move salesman algorithm here anyhow
    #TODO STEP7 - find a way for searching in the list for the path between given cities; it should be our distance calculation function
    #TODO STEP8 - perform traveling salesman on list of cities using distance calculation from STEP3
    #TODO STEP9 - draw everything

    locations = []
    locations.append(Location(2, 2, "Tomato"))
    locations.append(Location(15, 5, "Banana"))
    locations.append(Location(35, 8, "Oil"))
    locations.append(Location(23, 20, "Potatoes"))
    locations.append(Location(27, 27, "Carrot"))
    locations.append(Location(35, 30, "Bread"))
    locations.append(Location(27, 38, "Beer"))
    locations.append(Location(5, 39, "Rolls"))
    locations.append(Location(5, 44, "Wine"))
    locations.append(Location(15, 48, "MMs"))
    locations.append(Location(48, 48, "Water"))

    location_pairs = []
    for i, location in enumerate(locations):
        for j in range(i+1, len(locations)):
            location_pairs.append((location, locations[j]))

    i = 0
    while run:
        i = i % len(location_pairs)
        clock.tick(FPS)
        st = time.time()
        mygrid.solve_for_positions(*location_pairs[i])
        ex_time = time.time() - st
        dt = time.time()
        draw_window(mygrid)
        # print(f"Drawing took {time.time()-dt} seconds")
        # print(f"Solution for city pair no {i}, between city {location_pairs[i]} and {location_pairs[i]} found in {ex_time} seconds")
        pygame.time.wait(200)

        i += 1
        mygrid.reset_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # if i == len(location_pairs):
        #     break

    pygame.quit()

if __name__ == "__main__":
    main()
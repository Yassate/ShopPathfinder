from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid
from storage_types import Location

def draw_window(mygrid):
    WIN.fill(LGRAY)
    mygrid.draw()
    textfont = pygame.font.SysFont("monospace", 20)
    hello_text = textfont.render("Hola Amigo", 1, WHITE)
    WIN.blit(hello_text, (810, 20))
    pygame.display.update()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
LGRAY = (180, 180, 180)
FPS = 30
CITIES_COUNT = 10

def main():
    clock = pygame.time.Clock()
    run = True
    pygame.font.init()

    mygrid = AreaGrid(win=WIN, filepath="input_files/obstacles.txt", wh_pix=(WIDTH-200, HEIGHT))

    #Acceptance criteria - FLOW:
    #Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
    #List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
    #After clicking the product it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
    # "Find Path" triggers algorithm and shows path on the map
    # "Reset" causes deselecting of all products and clears the map

    #TODO #1 - create buttons on the right, pixel art, clickable buttons, like on youtube video 8SzTzvrWaAA

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

    for location in locations:
        mygrid.set_location(location)
    draw_window(mygrid)
    mygrid.reset_grid()

    for i in range(len(locations)-1):
        shortest = WIDTH+HEIGHT
        for j in range(i+1, len(locations)):
            dist = mygrid.get_shortest_length_between_locations(locations[i], locations[j])
            mygrid.reset_grid()
            if dist < shortest:
                shortest = dist
                nearest_p = locations[j]
        locations.remove(nearest_p)
        locations.insert(i+1, nearest_p)
    location_pairs = []
    for i in range(len(locations)-1):
        location_pairs.append((locations[i], locations[i+1]))

    i = 0
    while run:
        i = i % len(location_pairs)
        clock.tick(FPS)
        mygrid.solve_for_locations(*location_pairs[i])
        draw_window(mygrid)
        pygame.time.wait(500)

        i += 1
        # mygrid.reset_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # if i == len(location_pairs):
        #     break

    pygame.quit()

if __name__ == "__main__":
    main()

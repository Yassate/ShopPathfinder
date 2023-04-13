from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from storage_types import Location
from ui import AreaGrid, Button
from ui.colors import LGREY
from tsp import TrivialTSP
from astar import AStarSolver
import csv

HEIGHT = 750
GRID_WIDTH = HEIGHT
BUTTONS_WIDTH = round(1/4*GRID_WIDTH)
WIDTH = GRID_WIDTH + BUTTONS_WIDTH
CONST_BUTTON_W = 0.9*BUTTONS_WIDTH/2
CONST_BUTTON_H = 0.04*HEIGHT
MIN_SPACING = round(CONST_BUTTON_H/6) or 1
CONST_BUTTONS_Y = HEIGHT - CONST_BUTTON_H - 4*MIN_SPACING

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

# Acceptance criteria - FLOW:
# Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
# List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
# After clicking the aproduct it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
# "Find Path" triggers algorithm and shows path on the map
# "Reset" causes deselecting of all products and clears the map
# Usable multiple times

# TODO NEXT1 - docu?

def main():
    pygame.font.init()
    locations = read_locations("input_files/locations.csv")

    find_path_button, reset_button = init_func_buttons()
    loc_buttons = init_loc_buttons(locations, find_path_button.top_rect.topleft[1])

    ui_grid = AreaGrid(filepath="input_files/obstacles.txt", wh_pix=(GRID_WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    to_find: list[Location] = []

    while True:
        clock.tick(FPS)

        for button in loc_buttons:
            loc = get_loc_by_name(button.loc_name, locations)
            if button.pressed:
                if loc not in to_find:
                    to_find.append(loc)
                    ui_grid.set_location(loc)
            else:
                if loc in to_find:
                    to_find.remove(loc)
                    ui_grid.reset_location(loc)

        if reset_button.pressed:
            ui_grid.reset()
            for button in loc_buttons:
                button.pressed = False

        if find_path_button.pressed:
            astar = AStarSolver(ui_grid.get_org_grid())
            tsp = TrivialTSP(astar.get_shortest_length_between_locations, WIDTH*HEIGHT)
            solved = tsp.solve(to_find)
            location_pairs = []
            for i in range(len(solved)-1):
                location_pairs.append((solved[i], solved[i+1]))
            for loc_pair in location_pairs:
                path = astar.solve_for_locations(*loc_pair)
                ui_grid.set_path(path)
            find_path_button.pressed = False
        
        WIN.fill(LGREY)
        ui_grid.draw(WIN)
        for button in (loc_buttons + [find_path_button, reset_button]):
            button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

def read_locations(path):
    locations = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            locations.append(Location(int(row[1]), int(row[2]), row[0]))
    return locations

def init_loc_buttons(locations, func_buttons_top_left):
    loc_buttons = []
    loc_button_h = round(0.9*func_buttons_top_left/(4/3*len(locations)))
    loc_button_h = min(30, loc_button_h)
    vert_space = round(loc_button_h/3)
    for i, loc in enumerate(locations):
        loc_buttons.append(Button(loc.name, width=BUTTONS_WIDTH-2*MIN_SPACING, height=loc_button_h, pos=(GRID_WIDTH+MIN_SPACING, vert_space+(loc_button_h+vert_space)*i), bistable=True))
    return loc_buttons

def init_func_buttons():
    find_path_button = Button('Find path', CONST_BUTTON_W, CONST_BUTTON_H, (GRID_WIDTH+MIN_SPACING, CONST_BUTTONS_Y), bistable=False)
    reset_button = Button('Reset', CONST_BUTTON_W, CONST_BUTTON_H, (GRID_WIDTH+CONST_BUTTON_W+3*MIN_SPACING, CONST_BUTTONS_Y), bistable=False)
    return find_path_button,reset_button

def get_loc_by_name(name, locations):
    for loc in locations:
        if loc.name == name:
            return loc

if __name__ == "__main__":
    main()

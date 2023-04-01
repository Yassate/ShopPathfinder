from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from storage_types import Location
from ui import AreaGrid, Button
from ui.colors import LGREY
from typing import List
from tsp import TrivialTSP
from astar import AStarSolver

HEIGHT = 750
GRID_WIDTH = HEIGHT
BUTTONS_WIDTH = round(1/4*GRID_WIDTH)
WIDTH = GRID_WIDTH + BUTTONS_WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

def main():
    clock = pygame.time.Clock()
    run = True
    pygame.font.init()
    loc_buttons = []
    func_buttons = []
    mygrid = AreaGrid(filepath="input_files/obstacles.txt", wh_pix=(GRID_WIDTH, HEIGHT))

    const_buttons_width = 0.9*BUTTONS_WIDTH/2
    const_buttons_height = 0.04*HEIGHT
    min_spacing = round(const_buttons_height/6) or 1
    const_buttons_y = HEIGHT - const_buttons_height - 4*min_spacing
    find_path_button = Button('Find path', const_buttons_width, const_buttons_height, (GRID_WIDTH+min_spacing, const_buttons_y), bistable=False)
    reset_button = Button('Reset', const_buttons_width, const_buttons_height, (GRID_WIDTH+const_buttons_width+3*min_spacing, const_buttons_y), bistable=False)
    func_buttons.append(find_path_button)
    func_buttons.append(reset_button)

    # Acceptance criteria - FLOW:
    # Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
    # List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
    # After clicking the aproduct it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
    # "Find Path" triggers algorithm and shows path on the map
    # "Reset" causes deselecting of all products and clears the map
    # Usable multiple times

    # TODO NEXT0 - package tests with algorithms - salesman and pathfinder
    # TODO NEXT1 - move pathfinder from mygrid to separate package
    # TODO NEXT2 - refactor
    # TODO NEXT3 - Load list from file

    locations: List[Location] = []
    locations.append(Location(3, 3, "Tomato"))
    locations.append(Location(15, 6, "Banana"))
    locations.append(Location(35, 9, "Oil"))
    locations.append(Location(25, 23, "Potatoes"))
    locations.append(Location(26, 27, "Carrot"))
    locations.append(Location(35, 32, "Bread"))
    locations.append(Location(27, 40, "Beer"))
    locations.append(Location(4, 40, "Rolls"))
    locations.append(Location(4, 44, "Wine"))
    locations.append(Location(14, 47, "MMs"))
    locations.append(Location(44, 47, "Water"))

    button_height = round(0.9*find_path_button.top_rect.topleft[1]/(4/3*len(locations)))
    button_height = min(30, button_height)
    vert_space = round(button_height/3)

    for i, loc in enumerate(locations):
        loc_buttons.append(Button(loc.name, width=BUTTONS_WIDTH-2*min_spacing, height=button_height, pos=(GRID_WIDTH+min_spacing, vert_space+(button_height+vert_space)*i), bistable=True))

    def get_loc_by_name(name, locations):
        for loc in locations:
            if loc.name == name:
                return loc

    to_find: list[Location] = []

    while run:
        clock.tick(FPS)

        for button in loc_buttons:
            loc = get_loc_by_name(button.loc_name, locations)
            if button.pressed:
                if loc not in to_find:
                    to_find.append(loc)
                    mygrid.set_location(loc)
            else:
                if loc in to_find:
                    to_find.remove(loc)
                    mygrid.reset_location(loc)

        if reset_button.pressed:
            mygrid.reset_grid()
            for button in loc_buttons:
                button.pressed = False

        if find_path_button.pressed:
            astar = AStarSolver(mygrid.get_org_grid())
            tsp = TrivialTSP(astar.get_shortest_length_between_locations, WIDTH*HEIGHT)
            solved = tsp.solve(to_find)
            location_pairs = []
            for i in range(len(solved)-1):
                location_pairs.append((solved[i], solved[i+1]))
            for loc_pair in location_pairs:
                path = astar.solve_for_locations(*loc_pair)
                mygrid.set_path(path)
            find_path_button.pressed = False
        
        WIN.fill(LGREY)
        mygrid.draw(WIN)
        for button in (loc_buttons + func_buttons):
            button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()

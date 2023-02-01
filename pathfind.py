from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from a_star import AreaGrid
from storage_types import Location
from button import Button
from colors import LGREY
from typing import List

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
    mygrid = AreaGrid(win=WIN, filepath="input_files/obstacles.txt", wh_pix=(GRID_WIDTH, HEIGHT))

    const_buttons_width = 0.9*BUTTONS_WIDTH/2
    const_buttons_height = 0.04*HEIGHT
    min_spacing = round(const_buttons_height/6) or 1
    const_buttons_y = HEIGHT - const_buttons_height - 4*min_spacing
    
    find_path_button = Button('Find path', const_buttons_width, const_buttons_height, (GRID_WIDTH+min_spacing,const_buttons_y), bistable=False)
    reset_button = Button('Reset', const_buttons_width, const_buttons_height, (GRID_WIDTH+const_buttons_width+3*min_spacing,const_buttons_y), bistable=False)
    func_buttons.append(find_path_button)
    func_buttons.append(reset_button)


    # Acceptance criteria - FLOW:
    # Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
    # List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
    # After clicking the product it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
    # "Find Path" triggers algorithm and shows path on the map
    # "Reset" causes deselecting of all products and clears the map
    # Usable multiple times

    #TODO NEXT - WORK ON SELECT/DESELECT and RESET BUTTON (stays clicked and doesn't reset other buttons)
    #TODO NEXTNEXT - REFACTOR; it's a mess here
    #TODO NEXTNEXTNEXT - Load list from file 

    locations2 = {
        "Tomato":   Location(2,2),
        "Banana":   Location(15, 5),
        "Oil":      Location(35, 8),
        "Potatoes": Location(23, 20),
        "Carrot":   Location(27, 27),
        "Bread":    Location(35, 30),
        "Beer":     Location(27, 38),
        "Rolls":    Location(5, 39),
        "Wine":     Location(5, 44),
        "MMs":      Location(15, 48),
        "Water":    Location(48, 48)     
    }

    locations: List[Location] = []
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

    button_height = round(0.9*find_path_button.top_rect.topleft[1]/(4/3*len(locations)))
    button_height = min(30, button_height)

    vert_space = round(button_height/3)

    for i, loc in enumerate(locations):
        loc_buttons.append(Button(loc.name, width=BUTTONS_WIDTH-2*min_spacing, height=button_height, pos=(GRID_WIDTH+min_spacing, vert_space+(button_height+vert_space)*i), bistable=True))

    def get_loc_by_name(name, locations):
        for loc in locations:
            if loc.name == name:
                return loc

    to_find: List[Location] = []

    WIN.fill(LGREY)
    mygrid.draw()
    pygame.display.update()

    i = 0
    while run:
        to_find = []
        clock.tick(FPS)

        for button in loc_buttons:
            loc = get_loc_by_name(button.loc_name, locations)
            if button.pressed:
                to_find.append(loc)
                mygrid.set_location(loc)

        if find_path_button.pressed:
            for i in range(len(to_find)-1):
                shortest = WIDTH*HEIGHT
                for j in range(i+1, len(to_find)):
                    dist = mygrid.get_shortest_length_between_locations(to_find[i], to_find[j])
                    if dist < shortest:
                        shortest = dist
                        nearest_p = to_find[j]
                to_find.remove(nearest_p)
                to_find.insert(i+1, nearest_p)
            location_pairs = []
            for i in range(len(to_find)-1):
                location_pairs.append((to_find[i], to_find[i+1]))
            for loc_pair in location_pairs:
                mygrid.solve_for_locations(*loc_pair)
            find_path_button.pressed=False
        
        if reset_button.pressed:
            mygrid.reset_grid()


        WIN.fill(LGREY)
        mygrid.draw()
        for button in loc_buttons:
            button.draw(WIN)
        for button in func_buttons:
            button.draw(WIN)

        pygame.display.update()

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

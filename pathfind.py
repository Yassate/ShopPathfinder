from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid
from storage_types import Location
from Button import Button
from colors import LGREY

def draw_window(mygrid):
    WIN.fill(LGREY)
    mygrid.draw()
    # pygame.display.update()

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
    buttons = []
    mygrid = AreaGrid(win=WIN, filepath="input_files/obstacles.txt", wh_pix=(GRID_WIDTH, HEIGHT))

    const_buttons_width = 0.9*BUTTONS_WIDTH/2
    const_buttons_height = 0.04*HEIGHT
    min_spacing = round(const_buttons_height/6) or 1
    const_buttons_y = HEIGHT - const_buttons_height - 4*min_spacing
    print(const_buttons_height)
    print(min_spacing)
    
    find_path_button = Button('Find path', const_buttons_width, const_buttons_height, (GRID_WIDTH+min_spacing,const_buttons_y))
    reset_button = Button('Reset', const_buttons_width, const_buttons_height, (GRID_WIDTH+const_buttons_width+3*min_spacing,const_buttons_y))
    buttons.append(find_path_button)
    buttons.append(reset_button)


    #Acceptance criteria - FLOW:
    #Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
    #List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
    #After clicking the product it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
    # "Find Path" triggers algorithm and shows path on the map
    # "Reset" causes deselecting of all products and clears the map

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

    button_count = 15
    
    button_height = round(0.9*find_path_button.top_rect.topleft[1]/(4/3*button_count))
    if button_height>30:
        button_height=30

    vert_space = round(button_height/3)
    for i in range(button_count):
        buttons.append(Button("Temp", width=BUTTONS_WIDTH-2*min_spacing, height=button_height, pos=(GRID_WIDTH+min_spacing, vert_space+(button_height+vert_space)*i)))

    for location in locations:
        mygrid.set_location(location)
    draw_window(mygrid)
    mygrid.reset_grid()

    for i in range(len(locations)-1):
        shortest = WIDTH*HEIGHT
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
        for button in buttons:
            button.draw(WIN)

        pygame.display.update()
        pygame.time.wait(10)

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

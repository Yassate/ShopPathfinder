from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid
from storage_types import Location

def draw_window(mygrid):
    WIN.fill(LGREY)
    mygrid.draw()
    # pygame.display.update()

HEIGHT = 750
GRID_WIDTH = HEIGHT
BUTTONS_WIDTH = round(1/4*GRID_WIDTH)
WIDTH = GRID_WIDTH + BUTTONS_WIDTH
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
DGREEN = (24, 148, 92)
LGREY = (180, 180, 180)
DGREY = (100, 100, 100)
DDGREY = (70, 70, 70)

FPS = 30

class Button:
    def __init__(self, text, width, height, pos):
        self.color = DGREY
        self.font = pygame.font.Font(None, round(9/10*height))
        self.text_surf = self.font.render(text, True, WHITE)
        self.button_pressed = False
        self.mouse_pressed = False
        self.pos_y_default = pos[1]
        self.pos_y_pressed = pos[1] + round(height/6)

        self.top_rect = pygame.Rect(pos, (width, height))
        self.bottom_rect = pygame.Rect((pos[0], pos[1] + round(height/6)), (width, height))
        self.text_rect = self.text_surf.get_rect()

    def draw(self):
        self.click_detect()
        self._update_button_pos()
        pygame.draw.rect(WIN, DDGREY, self.bottom_rect, border_radius=10)
        pygame.draw.rect(WIN, self.color, self.top_rect, border_radius=10)
        pygame.draw.rect(WIN, WHITE, self.top_rect, width=1, border_radius=10)
        WIN.blit(self.text_surf, self.text_rect)

    def _update_button_pos(self):
        self.top_rect.y = self.pos_y_pressed if self.button_pressed else self.pos_y_default
        self.color = DGREEN if self.button_pressed else DGREY
        self.text_rect.center = self.top_rect.center

    def click_detect(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if(pygame.mouse.get_pressed()[0]):
                self.mouse_pressed = True
            else:
                if self.mouse_pressed == True:
                    self.button_pressed = not self.button_pressed
                    self.mouse_pressed = False

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
            button.draw()

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

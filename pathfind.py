from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from AStar import AreaGrid
from storage_types import Location

def draw_window(mygrid):
    WIN.fill(LGREY)
    mygrid.draw()
    # pygame.display.update()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
DGREEN = (24, 148, 92)
LGREY = (180, 180, 180)
DGREY = (100, 100, 100)
DDGREY = (70, 70, 70)

FPS = 30
CITIES_COUNT = 10

class Button:
    def __init__(self, text, width, height, pos):
        self.color = DGREY
        self.font = pygame.font.Font(None, round(4*height/5))
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
        pygame.draw.rect(WIN, DDGREY, self.bottom_rect, border_radius=12)
        pygame.draw.rect(WIN, self.color, self.top_rect, border_radius=12)
        pygame.draw.rect(WIN, WHITE, self.top_rect, width=1, border_radius=12)
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

    mygrid = AreaGrid(win=WIN, filepath="input_files/obstacles.txt", wh_pix=(WIDTH-200, HEIGHT))
    button1 = Button('Tomato', 160 ,30, (820,10))
    button2 = Button('Banana', 160 ,30, (820,50))
    button3 = Button('Oil', 160 ,30, (820,90))
    button4 = Button('Potatoes', 160 ,30, (820,130))

    #Acceptance criteria - FLOW:
    #Opening the app - you see the map and on the right side, short list of clickable product names + find path and reset button
    #List loadable from file, paths to file and map can be hardcoded/parameter of main or taken from script folder
    #After clicking the product it remains selected, until it's deselected. Both action causes to mark and unmark location on the map
    # "Find Path" triggers algorithm and shows path on the map
    # "Reset" causes deselecting of all products and clears the map

    #TODO #1 - create multiple buttons on the right, pixel art, clickable buttons, like on youtube video 8SzTzvrWaAA

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
        button1.draw()
        button2.draw()
        button3.draw()
        button4.draw()

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

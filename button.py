import pygame
from colors import WHITE, DGREY, DDGREY, DGREEN


class Button:
    def __init__(self, loc_name, width, height, pos, bistable):
        self.bistable = bistable
        self.loc_name = loc_name
        self.color = DGREY
        self.font = pygame.font.Font(None, round(9/10*height))
        self.text_surf = self.font.render(loc_name, True, WHITE)
        self.pressed = False
        self.mouse_pressed = False
        self.pos_y_default = pos[1]
        self.pos_y_pressed = pos[1] + round(height/6)

        self.top_rect = pygame.Rect(pos, (width, height))
        self.bottom_rect = pygame.Rect((pos[0], pos[1] + round(height/6)), (width, height))
        self.text_rect = self.text_surf.get_rect()

    def _update_button_pos(self):
        self.top_rect.y = self.pos_y_pressed if self.pressed else self.pos_y_default
        self.color = DGREEN if self.pressed else DGREY
        self.text_rect.center = self.top_rect.center

    def draw(self, WIN):
        self.click_detect()
        self._update_button_pos()
        pygame.draw.rect(WIN, DDGREY, self.bottom_rect, border_radius=10)
        pygame.draw.rect(WIN, self.color, self.top_rect, border_radius=10)
        pygame.draw.rect(WIN, WHITE, self.top_rect, width=1, border_radius=10)
        WIN.blit(self.text_surf, self.text_rect)

    def click_detect(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if not self.bistable:
                self.pressed = pygame.mouse.get_pressed()[0]
            if pygame.mouse.get_pressed()[0]:
                self.mouse_pressed = True
            else:
                if self.bistable:
                    if self.mouse_pressed:
                        self.pressed = not self.pressed
                self.mouse_pressed = False

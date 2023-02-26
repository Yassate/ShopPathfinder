import pygame
from ui.colors import WHITE, DGREY, DDGREY, DGREEN

class Button:
    def __init__(self, loc_name: str, width: int, height: int, pos: tuple[int, int], bistable: bool):
        self.loc_name = loc_name
        self.pressed = False
        self.top_rect = pygame.Rect(pos, (width, height))
        self._bistable = bistable
        self._color = DGREY
        self._font = pygame.font.Font(None, round(9/10*height))
        self._text_surf = self._font.render(loc_name, True, WHITE)
        self._mouse_pressed = False
        self._pos_y_default = pos[1]
        self._pos_y_pressed = pos[1] + round(height/6)
        self._bottom_rect = pygame.Rect((pos[0], pos[1] + round(height/6)), (width, height))
        self._text_rect = self._text_surf.get_rect()

    def draw(self, WIN: pygame.Surface):
        self._click_detect()
        self._update_button_pos()
        pygame.draw.rect(WIN, DDGREY, self._bottom_rect, border_radius=10)
        pygame.draw.rect(WIN, self.color, self.top_rect, border_radius=10)
        pygame.draw.rect(WIN, WHITE, self.top_rect, width=1, border_radius=10)
        WIN.blit(self._text_surf, self._text_rect)

    def _update_button_pos(self):
        self.top_rect.y = self._pos_y_pressed if self.pressed else self._pos_y_default
        self.color = DGREEN if self.pressed else DGREY
        self._text_rect.center = self.top_rect.center

    def _click_detect(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if not self._bistable:
                self.pressed = pygame.mouse.get_pressed()[0]
            if pygame.mouse.get_pressed()[0]:
                self._mouse_pressed = True
            else:
                if self._bistable:
                    if self._mouse_pressed:
                        self.pressed = not self.pressed
                self._mouse_pressed = False

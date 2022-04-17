import pygame
from settings import *

class e_list:
    def __init__(self,  surface):
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.background = pygame.Surface((screen_res[0] - self.wk_zone_res[0] - 30, screen_res[1] - 6))
        self.background.fill(((198, 198, 198, 255)))

    def draw(self):
        self.display_surface.blit(self.background, (3, 3))
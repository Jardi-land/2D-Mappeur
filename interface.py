import sys, pygame
from settings import *

class Interface:
    def __init__(self, surface) -> None:

        ####################
        #SURFACE DE WINDOWS#
        ####################
        self.display_surface = surface

        #################
        #ZONE DE TRAVAIL#
        #################
        #wk = work zone
        #ts = transparent
        #bg = back ground
        self.wk_zone_res = screen_res_array[screen_res_numb + 1]
        self.wk_ts_bg = pygame.transform.scale(pygame.image.load("mappeur_files/internal/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

    def draw(self):
        self.display_surface.blit(self.wk_ts_bg, (screen_res[0] - self.wk_zone_res[0], screen_res[1] - self.wk_zone_res[1]))
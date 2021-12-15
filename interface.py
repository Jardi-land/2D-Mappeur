import sys, pygame
from settings import *
from wk import work_zone
from interface_outline import outline_interface

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

        self.wk_class = work_zone(surface)
        self.outline_interface_class = outline_interface(surface)

        self.end_color = pygame.Surface((screen_res[0], screen_res[1]))
        self.end_color.fill(((101, 85, 97, 255)))

    def layout_2(self):

        self.display_surface.blit(self.end_color, (0, 0))

        self.wk_class.update()

    def layout_1(self):

        self.outline_interface_class.update()

    def draw(self):

        self.layout_2()

        self.layout_1()


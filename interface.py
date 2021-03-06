import pygame
import os
from settings import *
from wk import work_zone
from interface_outline import outline_interface
from menu import *


class Interface:
    def __init__(self, surface) -> None:

        ####################
        #SURFACE DE WINDOWS#
        ####################
        self.display_surface = surface

        #################
        #ZONE DE TRAVAIL#
        #################
        # wk = work zone
        #ts = transparent
        # bg = back ground
        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_class = work_zone(surface)
        self.outline_interface_class = outline_interface(surface)
        self.menu = menu(surface)

        self.end_color = pygame.Surface((screen_res[0], screen_res[1]))
        self.end_color.fill(((101, 85, 97, 255)))

        self.menu_check = True

        self.map_numb = 1

        self.action_list = []

        self.action_list.append(self.send_info)
        self.action_list.append(self.wk_class.update)
        self.action_list.append(self.outline_interface_class.update)
        self.action_list.append(self.menu.update)

    def fetch_name(self):
        while True:
            if os.path.exists(f"mappeur_files/map_/map_{self.map_numb}"):
                self.map_numb += 1
            else:
                return self.map_numb

    def send_info(self):
        self.wk_class.current_tool = self.outline_interface_class.out_worker_class.current_tool
        self.wk_class.single_action = self.outline_interface_class.out_worker_class.single_action
        self.outline_interface_class.out_worker_class.shortcut_status = self.wk_class.shortcut_status

    def action(self):
        if self.menu_check:
            if self.action_list[self.action_list.index(self.menu.update)]() is not None:
                self.action_list.pop(self.action_list.index(self.menu.update))
                del self.menu
                self.wk_class.wk_status = True
                self.wk_class.map_name = f"map_{self.fetch_name()}"
                os.makedirs(f"mappeur_files/map_/map_{self.map_numb}")
                self.wk_class.json_file()
                self.outline_interface_class.out_worker_class.button_status = True
                self.outline_interface_class.e_list.active = True
                self.menu_check = False

        self.display_surface.blit(self.end_color, (0, 0))

        for action in self.action_list:
            action()

    def draw(self):

        self.action()

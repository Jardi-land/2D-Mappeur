import sys
import pygame
from settings import *
from out_worker import out_worker


class outline_interface:
    def __init__(self, surface) -> None:
        self.display_surface = surface
        #######
        #LIGNE#
        #######
        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_corner = {"top-left": {"image": pygame.image.load("mappeur_files/internal/work_zone/corner/top_left.png").convert_alpha(),
                                       "pos": (screen_res[0] - self.wk_zone_res[0] - 8, screen_res[1] - self.wk_zone_res[1] - 8)},
                          "bottom-left": {"image": pygame.image.load("mappeur_files/internal/work_zone/corner/bottom_left.png").convert_alpha(),
                                          "pos": (screen_res[0] - self.wk_zone_res[0] - 8, screen_res[1] - 8)},
                          "top-right": {"image": pygame.image.load("mappeur_files/internal/work_zone/corner/top_right.png").convert_alpha(),
                                        "pos": (screen_res[0] - 8, screen_res[1] - self.wk_zone_res[1] - 8)},
                          "bottom-right": {"image": pygame.image.load("mappeur_files/internal/work_zone/corner/bottom_right.png").convert_alpha(),
                                           "pos": (screen_res[0] - 8, screen_res[1] - 8)}}

        self.wk_line = {"vertical": pygame.image.load("mappeur_files/internal/work_zone/line/vertical.png").convert_alpha(),
                        "horizontal": pygame.image.load("mappeur_files/internal/work_zone/line/horizontal.png").convert_alpha()}

        #################
        #"NOTHING-COLOR"#
        #################
        self.nothing_color_up = pygame.Surface(
            (screen_res[0], screen_res[1] - self.wk_zone_res[1] - 4))

        self.nothing_color_up.fill(((125, 146, 158, 255)))

        ############
        #OUT_WORKER#
        ############
        self.out_worker_class = out_worker(self.display_surface)

        self.wk_line["vertical"] = pygame.transform.scale(self.wk_line["vertical"], (self.wk_line["vertical"].get_width(
        ), (screen_res[1] - 9) - (screen_res[1] - self.wk_zone_res[1] - 7) - 6))
        self.wk_line["horizontal"] = pygame.transform.scale(self.wk_line["horizontal"], (screen_res[0] - 7 - (
            screen_res[0] - self.wk_zone_res[0] + 1), self.wk_line["horizontal"].get_height()))

        self.current_tool = "hand_tool"

        self.single_action = None

    def line(self):
        for i in self.wk_corner.keys():
            self.display_surface.blit(
                self.wk_corner[i]["image"], self.wk_corner[i]["pos"])

        self.display_surface.blit(self.wk_line["vertical"], (
            screen_res[0] - self.wk_zone_res[0] - 8, screen_res[1] - self.wk_zone_res[1]))

        self.display_surface.blit(
            self.wk_line["vertical"], (screen_res[0] - 6, screen_res[1] - self.wk_zone_res[1]))

        self.display_surface.blit(self.wk_line["horizontal"], (
            screen_res[0] - self.wk_zone_res[0], screen_res[1] - self.wk_zone_res[1] - 8))

        self.display_surface.blit(
            self.wk_line["horizontal"], (screen_res[0] - self.wk_zone_res[0], screen_res[1] - 6))

    def nothing_color(self):
        self.display_surface.blit(self.nothing_color_up, (screen_res[0] - self.wk_zone_res[0] - 8, 0))

    def worker_info_sharing(self):
        self.current_tool = self.out_worker_class.current_tool
        self.single_action = self.out_worker_class.single_action
        self.out_worker_class.single_action = None

    def update(self):
        self.worker_info_sharing()
        self.nothing_color()
        self.line()
        self.out_worker_class.update()

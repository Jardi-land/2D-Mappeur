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

        self.wk_ts_bg = pygame.transform.scale(pygame.image.load("mappeur_files/internal/work_zone/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

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

    def draw(self):
        self.display_surface.blit(self.wk_ts_bg, (screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4))

        for i in self.wk_corner.keys():
            self.display_surface.blit(self.wk_corner[i]["image"], self.wk_corner[i]["pos"])

        for i in range((screen_res[1] - 9) - (screen_res[1] - self.wk_zone_res[1] - 7) - 6):
            self.display_surface.blit(self.wk_line["vertical"], (screen_res[0] - self.wk_zone_res[0] - 8, screen_res[1] - self.wk_zone_res[1] + i))
            self.display_surface.blit(self.wk_line["vertical"], (screen_res[0] - 6, screen_res[1] - self.wk_zone_res[1] + i))

        for i in range((screen_res[0] - 7) - (screen_res[0] - self.wk_zone_res[0] + 1)):
            self.display_surface.blit(self.wk_line["horizontal"], (screen_res[0] - self.wk_zone_res[0] + i, screen_res[1] - self.wk_zone_res[1] - 8))
            self.display_surface.blit(self.wk_line["horizontal"], (screen_res[0] - self.wk_zone_res[0] + i, screen_res[1] - 6))


import sys, pygame
from settings import *

class outline_interface:
    def __init__(self, surface) -> None:
        super().__init__()
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
        self.nothing_color_up = pygame.Surface((screen_res[0], screen_res[1] - self.wk_zone_res[1]  - 4))
        self.nothing_color_down = pygame.Surface((screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1]))

        self.nothing_color_up.fill(((125, 146, 158, 255)))
        self.nothing_color_down.fill(((125, 146, 158, 255)))

    def line(self):
        for i in self.wk_corner.keys():
            self.display_surface.blit(self.wk_corner[i]["image"], self.wk_corner[i]["pos"])

        for i in range((screen_res[1] - 9) - (screen_res[1] - self.wk_zone_res[1] - 7) - 6):
            self.display_surface.blit(self.wk_line["vertical"], (screen_res[0] - self.wk_zone_res[0] - 8, screen_res[1] - self.wk_zone_res[1] + i))
            self.display_surface.blit(self.wk_line["vertical"], (screen_res[0] - 6, screen_res[1] - self.wk_zone_res[1] + i))

        for i in range((screen_res[0] - 7) - (screen_res[0] - self.wk_zone_res[0] + 1)):
            self.display_surface.blit(self.wk_line["horizontal"], (screen_res[0] - self.wk_zone_res[0] + i, screen_res[1] - self.wk_zone_res[1] - 8))
            self.display_surface.blit(self.wk_line["horizontal"], (screen_res[0] - self.wk_zone_res[0] + i, screen_res[1] - 6))

    def nothing_color(self):
        self.display_surface.blit(self.nothing_color_up, (0, 0))
        self.display_surface.blit(self.nothing_color_down, (0, 0))

    def update(self):
        self.nothing_color()
        self.line()
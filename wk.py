import sys, pygame
from settings import *

class work_zone:
    def __init__(self, surface) -> None:
        super().__init__()
        self.display_surface = surface
        #################
        #ZONE DE TRAVAIL#
        #################
        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_ts_bg = pygame.transform.scale(pygame.image.load("mappeur_files/internal/work_zone/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

        self.pos = pygame.math.Vector2(screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4)

        self.first_click_info = {"stop": False,
                                 "pos": (0, 0),
                                 "wk_ts_bg_pos": (0, 0)}

    def mouse_click(self, mouse):
        if mouse[0] > screen_res[0] - self.wk_ts_bg.get_width() and mouse[1] > screen_res[1] - self.wk_ts_bg.get_height():
            if pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False
        else:
            return False
    
    def draw(self, pos):
        self.display_surface.blit(self.wk_ts_bg, pos)

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        #pygame.mouse.set_pos(0, 0)

        if self.mouse_click(self.mouse):
            if not self.first_click_info["stop"]:
                self.first_click_info["pos"] = (self.mouse[0], self.mouse[1])
                self.first_click_info["wk_ts_bg_pos"] = (self.pos[0], self.pos[1])
                self.first_click_info["stop"] = True
            else:
                self.pos = (self.pos[0] + (self.mouse[0] - self.first_click_info["pos"][0]), self.pos[1] + (self.mouse[1] - self.first_click_info["pos"][1]))
                print("x :", self.mouse[0] - self.first_click_info["pos"][0], "| y :", self.mouse[1] - self.first_click_info["pos"][1])
                self.first_click_info["pos"] = (self.first_click_info["pos"][0] + (self.mouse[0] - self.first_click_info["pos"][0]), self.first_click_info["pos"][1] + (self.mouse[1] - self.first_click_info["pos"][1]))

        else:
            self.first_click_info["stop"] = False

        self.draw(self.pos)


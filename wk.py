from math import fabs
import sys, pygame
from tkinter.filedialog import SaveAs
from this import s
from settings import *
 # General information place
class wk_shard:
    def __init__(self, surface, info_place, zoom_array):
        self.display_surface = surface

        self.info_place = (info_place[0] * -1, info_place[1] * -1) # (x, x)

        self.zoom_array = zoom_array # Direct from zoom_table

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_ts_bg_og = pygame.transform.scale(pygame.image.load("mappeur_files/internal/work_zone/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

        self.size_og = (self.wk_ts_bg_og.get_width(), self.wk_ts_bg_og.get_height())
        
        self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg_og, (int(self.size_og[0] * self.zoom_array), int(self.size_og[1] * self.zoom_array)))

        self.og_pos = (screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4)

        if self.info_place == (0, 0):
            self.pos = self.og_pos
        else: self.pos = (self.og_pos[0] + (self.wk_ts_bg.get_width() * self.info_place[0]), self.og_pos[1] + (self.wk_ts_bg.get_height() * self.info_place[1]))

    def draw(self):
        self.display_surface.blit(self.wk_ts_bg, self.pos)

    def apply_mov(self, mov_vector):
        self.pos = (self.pos[0] + mov_vector[0], self.pos[1] + mov_vector[1])

    def apply_zoom(self, size, pos):
        self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg_og, (size))
        self.pos = (pos[0] + (self.wk_ts_bg.get_width() * self.info_place[0]), pos[1] + (self.wk_ts_bg.get_height() * self.info_place[1]))

class work_zone:
    def __init__(self, surface) -> None:
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_ts_bg_og = pygame.transform.scale(pygame.image.load("mappeur_files/internal/work_zone/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

        self.wk_ts_bg = self.wk_ts_bg_og

        self.pos = (screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4)

        self.size_og = (self.wk_ts_bg_og.get_width(), self.wk_ts_bg_og.get_height())

        self.single_input = {"left_click": True, "right_click": True}

        self.size = self.size_og

        self.zoom_array = 0

        self.zoom_array_max = 10

        self.zoom_table = {10: 2, 9: 1.9, 8: 1.8, 7: 1.7, 6: 1.6, 5: 1.5, 4: 1.4, 3: 1.3, 2: 1.2, 1: 1.1, 0: 1, -1: 0.9, -2: 0.8, -3: 0.7, -4: 0.6, -5: 0.5, -6: 0.4, -7: 0.3, -8: 0.2, -9: 0.1, -10: 0.09}

        self.first_click_info = {"stop": False,
                                 "pos": (0, 0),
                                 "wk_ts_bg_pos": (0, 0)}

        self.current_tool = "hand_tool"

        self.wk_list = []

        self.wk_list.append(wk_shard(self.display_surface, (0, 0), self.zoom_table[self.zoom_array]))

    def mouse_click(self, mouse, click_type, use_single = False):
        if mouse[0] > screen_res[0] - self.size_og[0] and mouse[1] > screen_res[1] - self.size_og[1]:
            if click_type == "left":
                if pygame.mouse.get_pressed()[0]:
                    if use_single:
                        if self.single_input["left_click"]:
                            self.single_input["left_click"] = False
                            return True
                        else: return False
                    else: return True
                else:
                    self.single_input["left_click"] = True
                    return False
            elif click_type == "right":
                if pygame.mouse.get_pressed()[2]:
                    if use_single:
                        if self.single_input["right_click"]:
                            self.single_input["right_click"] = False
                            return True
                        else: return False
                    else: return True
                else:
                    self.single_input["right_click"] = True
                    return False
            elif click_type == "any" and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
                if use_single:
                    print("ERROR: pas de use_single pour le click type: any")
                return True
            else:
                return False
        else:
            return False

    def tool_info_sharing(self, tool):
        self.current_tool = tool
    
    def draw(self):
        for i in self.wk_list:
            i.draw()

    def hand_tool(self, mouse):
        if self.mouse_click(mouse, "any"):
            if not self.first_click_info["stop"]:
                self.first_click_info["pos"] = (mouse[0], mouse[1])
                self.first_click_info["wk_ts_bg_pos"] = (self.pos[0], self.pos[1])
                self.first_click_info["stop"] = True
            else:
                for i in self.wk_list:
                    i.apply_mov(((mouse[0] - self.first_click_info["pos"][0]), (mouse[1] - self.first_click_info["pos"][1])))
                self.pos = (self.pos[0] + (mouse[0] - self.first_click_info["pos"][0]), self.pos[1] + (mouse[1] - self.first_click_info["pos"][1]))
                self.first_click_info["pos"] = (self.first_click_info["pos"][0] + (mouse[0] - self.first_click_info["pos"][0]), self.first_click_info["pos"][1] + (mouse[1] - self.first_click_info["pos"][1]))

        else:
            self.first_click_info["stop"] = False

    def zoom_tool(self, mouse):
        if self.mouse_click(mouse, "left", True):
            self.zoom_type = "in"
        elif self.mouse_click(mouse, "right", True):
            self.zoom_type = "out"
        else: 
            self.zoom_type = None

        if not self.zoom_type == None:
            if self.zoom_type == "in":
                if self.zoom_array == self.zoom_array_max:
                    pass
                else:
                    self.old_zoom_array = self.zoom_array
                    self.zoom_array += 1
                    self.size = (int(self.size_og[0] * self.zoom_table[self.zoom_array]), int(self.size_og[1] * self.zoom_table[self.zoom_array]))
                    self.mouse_vector = ((screen_res[0] - self.wk_zone_res[0] - 4) - mouse[0], (screen_res[1] - self.wk_zone_res[1] - 4) - mouse[1])
                    self.pos = (int(mouse[0] + ((self.pos[0] - mouse[0]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array]))), int(mouse[1] + ((self.pos[1] - mouse[1]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array]))))
                    for i in self.wk_list:
                        i.apply_zoom(self.size, self.pos)
                    self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg_og, (self.size))
            elif self.zoom_type == "out":
                if self.zoom_array == self.zoom_array_max * -1:
                    pass
                else:
                    self.old_zoom_array = self.zoom_array
                    self.zoom_array -= 1
                    self.size = (int(self.size_og[0] * self.zoom_table[self.zoom_array]), int(self.size_og[1] * self.zoom_table[self.zoom_array]))
                    self.mouse_vector = ((screen_res[0] - self.wk_zone_res[0] - 4) - mouse[0], (screen_res[1] - self.wk_zone_res[1] - 4) - mouse[1])
                    self.pos = (int(mouse[0] + ((self.pos[0] - mouse[0]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array]))), int(mouse[1] + ((self.pos[1] - mouse[1]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array]))))
                    for i in self.wk_list:
                        i.apply_zoom(self.size, self.pos)
                    self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg_og, (self.size))

    def current_action(self, mouse):
        if self.current_tool == "hand_tool":
            self.hand_tool(mouse)
        elif self.current_tool == "zoom_tool":
            self.zoom_tool(mouse)

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        self.current_action(self.mouse)

        self.draw()


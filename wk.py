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

        self.size_og = (self.wk_ts_bg.get_width(), self.wk_ts_bg.get_height())

        self.single_input = {"left_click": True, "right_click": True}

        self.size = self.size_og

        self.zoom_array = 0

        self.zoom_array_max = 5

        self.zoom_table = {5: 2, 4: 1.8, 3: 1.6, 2: 1.4, 1: 1.2, 0: 1, -1: 0.8, -2: 0.6, -3: 0.4, -4: 0.2, -5: 0.1}

        self.first_click_info = {"stop": False,
                                 "pos": (0, 0),
                                 "wk_ts_bg_pos": (0, 0)}

        self.current_tool = "hand_tool"

    def mouse_click(self, mouse, click_type, use_single):
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
    
    def draw(self, pos):
        self.display_surface.blit(self.wk_ts_bg, pos)

    def hand_tool(self, mouse):
        if self.mouse_click(mouse, "any", False):
            if not self.first_click_info["stop"]:
                self.first_click_info["pos"] = (mouse[0], mouse[1])
                self.first_click_info["wk_ts_bg_pos"] = (self.pos[0], self.pos[1])
                self.first_click_info["stop"] = True
            else:
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
                    self.zoom_array += 1
                    self.size = (int(self.size_og[0] * self.zoom_table[self.zoom_array]), int(self.size_og[1] * self.zoom_table[self.zoom_array]))
                    self.mouse_pos = (mouse[0], mouse[1])
                    self.mouse_vector = ((screen_res[0] - self.wk_zone_res[0] - 4) - mouse[0], (screen_res[1] - self.wk_zone_res[1] - 4) - mouse[1])
                    self.pos = (int(mouse[0] + (self.mouse_vector[0] * self.zoom_table[self.zoom_array])), int(mouse[1] + (self.mouse_vector[1] * self.zoom_table[self.zoom_array])))
                    self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg, (self.size))
            elif self.zoom_type == "out":
                if self.zoom_array == self.zoom_array_max * -1:
                    pass
                else:
                    self.zoom_array -= 1
                    self.size = (int(self.size_og[0] * self.zoom_table[self.zoom_array]), int(self.size_og[1] * self.zoom_table[self.zoom_array]))
                    self.mouse_pos = (mouse[0], mouse[1])
                    self.mouse_vector = ((screen_res[0] - self.wk_zone_res[0] - 4) - mouse[0], (screen_res[1] - self.wk_zone_res[1] - 4) - mouse[1])
                    self.pos = (int(mouse[0] + (self.mouse_vector[0] * self.zoom_table[self.zoom_array])), int(mouse[1] + (self.mouse_vector[1] * self.zoom_table[self.zoom_array])))
                    self.wk_ts_bg = pygame.transform.scale(self.wk_ts_bg, (self.size))



    def current_action(self, mouse):
        if self.current_tool == "hand_tool":
            self.hand_tool(mouse)
        elif self.current_tool == "zoom_tool":
            self.zoom_tool(mouse)

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        self.current_action(self.mouse)

        self.draw(self.pos)


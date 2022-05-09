import pygame
from settings import *


class spawn_point:
    def __init__(self, surface, zoom_array):
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.zoom_array = zoom_array

        self.spawn_icon_og = pygame.image.load(
            "mappeur_files/internal/work_zone/spawn/spawn_point.png").convert_alpha()

        self.spawn_icon = pygame.transform.scale(self.spawn_icon_og, (int(self.spawn_icon_og.get_width(
        ) * self.zoom_array), int(self.spawn_icon_og.get_height() * self.zoom_array)))

        self.pos_og = (960, 540)  # On a 1920 x 1080 resolution
        self.pos = (0, 0)

    def apply_zoom(self, size):
        self.spawn_icon = pygame.transform.scale(self.spawn_icon_og, (
            self.spawn_icon_og.get_width() * size, self.spawn_icon_og.get_height() * size))

    def draw(self):
        self.display_surface.blit(self.spawn_icon, (self.pos[0] - (
            self.spawn_icon.get_width() / 2), self.pos[1] - (self.spawn_icon.get_height() / 2)))


class work_zone:
    def __init__(self, surface) -> None:
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.wk_ts_bg_og = pygame.transform.scale(pygame.image.load(
            "mappeur_files/internal/work_zone/bg/transparent_background.png").convert_alpha(), (int(self.wk_zone_res[0]), int(self.wk_zone_res[1])))

        self.wk_ts_bg = self.wk_ts_bg_og

        self.pos = (screen_res[0] - self.wk_zone_res[0] - 4,
                    screen_res[1] - self.wk_zone_res[1] - 4)

        self.size_og = (self.wk_ts_bg_og.get_width(),
                        self.wk_ts_bg_og.get_height())

        self.single_input = {"left_click": True, "right_click": True}

        self.size = self.size_og

        self.zoom_array = 0

        self.zoom_array_max = 10

        self.zoom_table = {10: 2, 9: 1.9, 8: 1.8, 7: 1.7, 6: 1.6, 5: 1.5, 4: 1.4, 3: 1.3, 2: 1.2, 1: 1.1,
                           0: 1, -1: 0.9, -2: 0.8, -3: 0.7, -4: 0.6, -5: 0.5, -6: 0.4, -7: 0.3, -8: 0.2, -9: 0.1, -10: 0.09}

        self.first_click_info = {"stop": False,
                                 "pos": (0, 0),
                                 "wk_ts_bg_pos": (0, 0)}

        self.first_click_info_spawn = {"stop": False,
                                       "pos": (0, 0),
                                       "spawn_point_pos": (0, 0)}

        self.current_tool = "hand_tool"

        self.single_action = None

        self.spawn_point = spawn_point(
            self.display_surface, self.zoom_table[self.zoom_array])

        self.draw_spawn_point = False

        self.wk_status = False

    def mouse_click(self, mouse, click_type, use_single=False):
        if mouse[0] > screen_res[0] - self.size_og[0] and mouse[1] > screen_res[1] - self.size_og[1]:
            if click_type == "left":
                if pygame.mouse.get_pressed()[0]:
                    if use_single:
                        if self.single_input["left_click"]:
                            self.single_input["left_click"] = False
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    self.single_input["left_click"] = True
                    return False
            elif click_type == "right":
                if pygame.mouse.get_pressed()[2]:
                    if use_single:
                        if self.single_input["right_click"]:
                            self.single_input["right_click"] = False
                            return True
                        else:
                            return False
                    else:
                        return True
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

    def trans_pos(self, pos_base, reverse=False):
        if not reverse:
            try:
                return (self.pos[0] + (self.wk_ts_bg.get_width() / (1920 / pos_base[0])), self.pos[1] + (self.wk_ts_bg.get_height() / (1080 / pos_base[1])))
            except ZeroDivisionError:
                if pos_base[0] == 0 and pos_base[1] == 0:
                    return (self.pos[0], self.pos[1])
                elif pos_base[0] == 0:
                    return (self.pos[0], self.pos[1] + (self.wk_ts_bg.get_height() / (1080 / pos_base[1])))
                elif pos_base[1] == 0:
                    return (self.pos[0] + (self.wk_ts_bg.get_width() / (1920 / pos_base[0])), self.pos[1])
        else:
            try:
                return (1920 / (self.wk_ts_bg.get_width() / (pos_base[0] - self.pos[0])), 1080 / (self.wk_ts_bg.get_height() / (pos_base[1] - self.pos[1])))
            except ZeroDivisionError:
                if pos_base[0] == self.pos[0] and pos_base[1] == self.pos[1]:
                    return (0, 0)
                elif pos_base[0] == self.pos[0]:
                    return (0, 1080 / (self.wk_ts_bg.get_height() / (pos_base[1] - self.pos[1])))
                elif pos_base[1] == self.pos[1]:
                    return (1920 / (self.wk_ts_bg.get_width() / (pos_base[0] - self.pos[0])), 0)

    def draw(self):
        if not self.wk_status:
            pass
        else:
            self.display_surface.blit(self.wk_ts_bg, self.pos)

            if self.draw_spawn_point:
                self.spawn_point.draw()
            if not self.current_tool == "spawn_point":
                self.draw_spawn_point = False

    def hand_tool(self, mouse):
        if self.mouse_click(mouse, "any"):
            if not self.first_click_info["stop"]:
                self.first_click_info["pos"] = (mouse[0], mouse[1])
                self.first_click_info["wk_ts_bg_pos"] = (
                    self.pos[0], self.pos[1])
                self.first_click_info["stop"] = True
            else:
                self.pos = (self.pos[0] + (mouse[0] - self.first_click_info["pos"][0]),
                            self.pos[1] + (mouse[1] - self.first_click_info["pos"][1]))
                self.first_click_info["pos"] = (self.first_click_info["pos"][0] + (mouse[0] - self.first_click_info["pos"][0]),
                                                self.first_click_info["pos"][1] + (mouse[1] - self.first_click_info["pos"][1]))

        else:
            self.first_click_info["stop"] = False

        if self.single_action == "center":
            self.pos = ((screen_res[0] - self.wk_zone_res[0] - 4) + (self.wk_zone_res[0] / 2) - (self.wk_ts_bg.get_width() / 2),
                        (screen_res[1] - self.wk_zone_res[1] - 4) + (self.wk_zone_res[1] / 2) - (self.wk_ts_bg.get_height() / 2))

    def zoom_tool(self, mouse):
        if self.mouse_click(mouse, "left", True):
            self.zoom_type = "in"
        elif self.mouse_click(mouse, "right", True):
            self.zoom_type = "out"
        else:
            self.zoom_type = None

        def zooming_process(self, type):
            if (type == "in" and self.zoom_array == self.zoom_array_max) or (type == "out" and self.zoom_array == self.zoom_array_max * -1):
                pass
            else:
                self.old_zoom_array = self.zoom_array
                self.zoom_array += 1 if type == "in" else -1
                self.size = (int(self.size_og[0] * self.zoom_table[self.zoom_array]), int(
                    self.size_og[1] * self.zoom_table[self.zoom_array]))
                self.pos = (mouse[0] + ((self.pos[0] - mouse[0]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array])),
                            mouse[1] + ((self.pos[1] - mouse[1]) * (self.zoom_table[self.zoom_array] / self.zoom_table[self.old_zoom_array])))
                self.wk_ts_bg = pygame.transform.scale(
                    self.wk_ts_bg_og, (self.size))
                self.spawn_point.apply_zoom(
                    self.zoom_table[self.zoom_array])

        if not self.zoom_type == None:
            zooming_process(self, self.zoom_type)

        if self.single_action == "center":
            self.zoom_array = 0
            self.wk_ts_bg = pygame.transform.scale(
                self.wk_ts_bg_og, (self.size_og))
            self.spawn_point.apply_zoom(
                self.zoom_table[self.zoom_array])
            self.pos = (screen_res[0] - self.wk_zone_res[0] - 4,
                        screen_res[1] - self.wk_zone_res[1] - 4)

    def spawn_tool(self, mouse):
        self.draw_spawn_point = True
        self.spawn_point.pos = self.trans_pos(self.spawn_point.pos_og)

        if self.single_action == "center":
            self.spawn_point.pos_og = (960, 540)

        if self.mouse_click(mouse, "any"):
            if not self.first_click_info_spawn["stop"]:
                self.first_click_info_spawn["pos"] = (mouse[0], mouse[1])
                self.first_click_info_spawn["spawn_point_pos"] = (
                    self.spawn_point.pos_og[0], self.spawn_point.pos_og[1])
                self.first_click_info_spawn["stop"] = True
            else:
                self.spawn_point.pos_og = (self.trans_pos(self.spawn_point.pos, True)[0] + (1920 / self.wk_ts_bg.get_width()) * (mouse[0] - self.first_click_info_spawn["pos"][0]), self.trans_pos(
                    self.spawn_point.pos, True)[1] + (1080 / self.wk_ts_bg.get_height()) * (mouse[1] - self.first_click_info_spawn["pos"][1]))
                self.first_click_info_spawn["pos"] = (self.first_click_info_spawn["pos"][0] + (mouse[0] - self.first_click_info_spawn["pos"][0]),
                                                      self.first_click_info_spawn["pos"][1] + (mouse[1] - self.first_click_info_spawn["pos"][1]))

        else:
            self.first_click_info_spawn["stop"] = False

    def current_action(self, mouse):
        if self.current_tool == "hand_tool":
            self.hand_tool(mouse)
        elif self.current_tool == "zoom_tool":
            self.zoom_tool(mouse)
        elif self.current_tool == "spawn_tool":
            self.spawn_tool(mouse)

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        self.current_action(self.mouse)

        self.draw()

import sys
import pygame
from settings import *


class button:
    def __init__(self, surface, type, action, img_path, img_selec_path, x, y, transx, transy, shortcut, appear_event=[False]) -> None:
        self.display_surface = surface

        self.type = type

        self.action = action

        self.appear_event = appear_event

        self.default_image = pygame.image.load(img_path).convert_alpha()

        self.alternate_image = pygame.image.load(
            img_selec_path).convert_alpha()

        self.image = self.default_image

        self.pos = (x, y)

        self.size = (transx, transy)

        self.shortcut = shortcut

        self.shortcut_status = True

    def is_over(self, mouse):
        if mouse[0] > self.pos[0] and mouse[0] < (self.pos[0] + self.image.get_width()) and mouse[1] > self.pos[1] and mouse[1] < (self.pos[1] + self.image.get_height()):
            return True
        else:
            return False

    def get_action(self, mouse, current_tool, button_status):
        self.keys = pygame.key.get_pressed()
        if not button_status:
            return None
        else:
            if not current_tool == self.action:
                if self.shortcut == None:
                    if pygame.mouse.get_pressed()[0] and self.is_over(mouse):
                        return self.action
                    else:
                        return None
                else:
                    if (pygame.mouse.get_pressed()[0] and self.is_over(mouse)) or (self.keys[self.shortcut] if self.shortcut_status else False):
                        return self.action
                    else:
                        return None
            else:
                return None

    def update(self, mouse, current_tool, button_status, alpha=1):
        if not button_status:
            self.image = self.default_image
            self.image.set_alpha(255 * 0.5)
        else:
            if not alpha == 1:
                self.image.set_alpha(255 * alpha)
            else:
                self.image.set_alpha(255)
                if self.is_over(mouse) or current_tool == self.action:
                    self.image = self.alternate_image
                else:
                    self.image = self.default_image
        self.display_surface.blit(self.image, self.pos)


class out_worker:
    def __init__(self, surface) -> None:
        super().__init__()
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.current_tool = None

        self.single_action = None

        self.button_size = (32, 32)

        self.first_button_pos = (screen_res[0] - self.button_size[0] - 2, screen_res[1] -
                                 self.wk_zone_res[1] - 10 - self.button_size[1], self.button_size[0])

        self.button_status = False

        self.shortcut_status = True

        self.button_list = []

        # All button
        self.hand_tool = button(self.display_surface, "tool", "hand_tool", "mappeur_files/internal/out_worker/button/hand_tool/unselected.png",
                                "mappeur_files/internal/out_worker/button/hand_tool/selected.png", self.first_button_pos[0], self.first_button_pos[1], self.button_size[0], self.button_size[1], pygame.K_h)
        self.button_list.append(self.hand_tool)

        self.zoom_tool = button(self.display_surface, "tool", "zoom_tool", "mappeur_files/internal/out_worker/button/zoom_tool/unselected.png", "mappeur_files/internal/out_worker/button/zoom_tool/selected.png",
                                self.first_button_pos[0] - (self.button_size[0] - 2), self.first_button_pos[1], self.button_size[0], self.button_size[1], pygame.K_z)
        self.button_list.append(self.zoom_tool)

        self.spawn_tool = button(self.display_surface, "tool", "spawn_tool", "mappeur_files/internal/out_worker/button/spawn_tool/unselected.png", "mappeur_files/internal/out_worker/button/spawn_tool/selected.png",
                                 self.first_button_pos[0] - (2 * (self.button_size[0] - 2)), self.first_button_pos[1], self.button_size[0], self.button_size[1], pygame.K_s)
        self.button_list.append(self.spawn_tool)

        self.center_button = button(self.display_surface, "single_action", "center", "mappeur_files/internal/out_worker/button/center_button/unselected.png", "mappeur_files/internal/out_worker/button/center_button/selected.png",
                                    self.first_button_pos[0], self.first_button_pos[1] - (self.button_size[0] - 2), self.button_size[0], self.button_size[1], None, ["hand_tool", "zoom_tool", "spawn_tool"])
        self.button_list.append(self.center_button)

        self.new_group = button(self.display_surface, "single_action", "new_group", "mappeur_files/internal/out_worker/button/new_group_button/unselected.png",
                                "mappeur_files/internal/out_worker/button/new_group_button/selected.png", screen_res[0] - self.wk_zone_res[0] - 8, self.first_button_pos[1], self.button_size[0], self.button_size[1], pygame.K_n, [False])
        self.button_list.append(self.new_group)

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()

        for i in self.button_list:
            i.shortcut_status = self.shortcut_status
            if i.type == "tool":
                if not i.get_action(self.mouse, self.current_tool, self.button_status) == None:
                    self.current_tool = i.get_action(
                        self.mouse, self.current_tool, self.button_status)
                i.update(self.mouse, self.current_tool, self.button_status)

            elif i.type == "single_action":
                if not i.get_action(self.mouse, self.current_tool, self.button_status) == None:
                    self.single_action = i.get_action(
                        self.mouse, self.current_tool, self.button_status)
                if self.current_tool in i.appear_event or False in i.appear_event:
                    i.update(self.mouse, self.current_tool, self.button_status)
                else:
                    i.update(self.mouse, self.current_tool,
                             self.button_status, 0.5)

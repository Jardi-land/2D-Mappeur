import sys, pygame
from typing import overload
from settings import *

class button:
    def __init__(self, surface, type, img_path, img_selec_path, x, y, transx, transy) -> None:
        self.display_surface = surface
        
        self.type = type

        self.default_image = pygame.image.load(img_path).convert_alpha()

        self.alternate_image = pygame.image.load(img_selec_path).convert_alpha()

        self.image = self.default_image

        self.pos = (x, y)

        self.size = (transx, transy)

    def is_over(self, mouse):
        if mouse[0] > self.pos[0] and mouse[0] < (self.pos[0] + self.image.get_width()) and mouse[1] > self.pos[1] and mouse[1] < (self.pos[1] + self.image.get_height()):
            return True
        else: 
            return False

    def get_tool(self, mouse, current_tool):
        if self.is_over(mouse):
            if not current_tool == self.type:
                if pygame.mouse.get_pressed()[0]:
                    return self.type
                else:
                    return None
            else:
                return None
        else:
            return None

    def update(self, mouse, current_tool):
        if self.is_over(mouse) or current_tool == self.type:
            self.image = self.alternate_image
        else:
            if not current_tool == self.type:
                self.image = self.default_image
        self.display_surface.blit(self.image, self.pos)
        
        

class out_worker:
    def __init__(self, surface) -> None:
        super().__init__()
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.current_tool = "hand_tool"

        self.button_size = (32, 32)

        self.first_button_pos = (screen_res[0] - self.button_size[0] - 2, screen_res[1] - self.wk_zone_res[1] - 10 - self.button_size[1], self.button_size[0])

        #All button
        self.hand_tool = button(self.display_surface, "hand_tool", "mappeur_files/internal/out_worker/button/hand_tool/unselected.png", "mappeur_files/internal/out_worker/button/hand_tool/selected.png", self.first_button_pos[0], self.first_button_pos[1], self.button_size[0], self.button_size[1])

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        if not self.hand_tool.get_tool(self.mouse, self.current_tool) == None:
            self.current_tool = self.hand_tool.get_tool(self.mouse, self.current_tool)
        self.hand_tool.update(self.mouse, self.current_tool)
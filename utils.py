import pygame
import json
from settings import *


def palette_swap(surf, old_color, new_color):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_color)
    surf.set_colorkey(old_color)
    img_copy.blit(surf, (0, 0))
    return img_copy


class Spritesheet:
    def __init__(self, filename, old_color=(255, 255, 255), new_color=(255, 255, 255)):
        self.filename = filename
        self.sprite_sheet = palette_swap(pygame.image.load(
            filename).convert_alpha(), old_color, new_color)
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((255, 255, 255))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image


class text:
    def __init__(self, surface, string, size, pos, color=(0, 0, 0), max_with=1920):

        self.display_surface = surface

        self.pos = pos

        self.color = color

        self.text_image = {}

        self.line_width = {}

        self.spritesheet = Spritesheet(
            "mappeur_files/internal/text/spritesheet.png", (0, 0, 0), color)

        with open("mappeur_files/internal/text/spritesheet.json", encoding="utf8") as f:
            self.data = json.load(f)

        for cara in list(self.data["frames"].keys()):
            self.text_image[cara] = self.spritesheet.parse_sprite(cara)

        self.possible_cara = self.data["frames"].keys()

        self.text = string

        self.size = size

        if "\n" in self.text:
            self.text = self.text.split("\n")
        else:
            self.text = [self.text]

        for line in self.text:
            for cara in line:
                if cara not in self.possible_cara:
                    self.text = string.replace(cara, "þ")

        for line_nb, line in enumerate(self.text):
            self.line_width[line_nb] = 0
            for cara_nb, cara in enumerate(line):
                self.line_width[line_nb] += self.text_image[cara].get_width() * \
                    size

        def remove_last_word(line, i):
            self.line_created = False
            for cara_nb in range(len(line)):
                if list(reversed(line))[cara_nb] == " ":
                    self.text[i] = "".join(
                        reversed(list(reversed(line))[cara_nb:])).strip()
                    try:
                        self.text[i + 1] = " ".join(
                            ["".join(reversed(list(reversed(line))[:cara_nb])), self.text[i + 1]])
                    except IndexError:
                        self.text.append(
                            "".join(reversed(list(reversed(line))[:cara_nb])))
                        self.line_created = True
                    self.line_width[i] = 0
                    self.line_width[i + 1] = 0
                    for cara_2 in self.text[i]:
                        self.line_width[i] += self.text_image[cara_2].get_width() * \
                            size
                    for cara_2 in self.text[i + 1]:
                        self.line_width[i +
                                        1] += self.text_image[cara_2].get_width() * size
                    return self.line_created

        def new_line():
            self.line_width_copy = self.line_width.copy()
            for i in self.line_width_copy:
                while int(self.line_width[i]) > int(max_with):
                    if remove_last_word(self.text[i], i):
                        new_line()

        new_line()

        if self.text[-1] == "":
            del self.text[-1]
            del self.line_width[list(self.line_width.keys())[-1]]

    def get_height(self):
        return len(self.line_width) * 8 * self.size

    def get_width(self):
        return max(self.line_width.values())

    def draw(self):
        for line_nb, line in enumerate(self.text):
            self.pos_x = self.pos[0]
            for cara in line:
                self.display_surface.blit(pygame.transform.scale(self.text_image[cara], (self.text_image[cara].get_width(
                ) * self.size, self.text_image[cara].get_height() * self.size)), (self.pos_x, self.pos[1] + (8 * self.size * line_nb)))
                self.pos_x += self.text_image[cara].get_width() * self.size


class button:
    def __init__(self, surface, x, y, width=40, height=20, string=" ", font_size=1, action=None, unactive=0):
        self.display_surface = surface

        self.action = action

        self.unactive_time = unactive

        self.active = True if unactive == 0 else False

        self.button_img = {"top_left": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/top_left.png"),
                           "top_right": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/top_right.png"),
                           "bottom_left": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/bottom_left.png"),
                           "bottom_right": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/bottom_right.png"),
                           "bottom": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/bottom.png"),
                           "top": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/top.png"),
                           "left": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/left.png"),
                           "right": pygame.image.load("mappeur_files/internal/out_worker/button/button_template/right.png"),

                           "white": pygame.Surface((1, 1)),
                           "grey": pygame.Surface((1, 1))}

        self.button_img["white"].fill((255, 255, 255))
        self.button_img["grey"].fill((198, 198, 198))

        self.position = {"x": x - width / 2,
                         "y": y - height / 2,
                         "width": width,
                         "height": height}

        self.my_text = text(surface, string, font_size,
                            (x, y), (0, 0, 0), width)

        self.my_text = text(surface, string, font_size, (x - self.my_text.get_width() /
                            2, y - self.my_text.get_height() / 2), (0, 0, 0), width)

    def is_over(self):
        self.mouse = pygame.mouse.get_pos()
        if not self.active:
            return False
        else:
            if self.mouse[0] > self.position["x"] and self.mouse[0] < self.position["x"] + self.position["width"] and self.mouse[1] > self.position["y"] and self.mouse[1] < self.position["y"] + self.position["height"]:
                return True
            else:
                return False

    def is_pressed(self):
        if not self.active:
            pass
        else:
            if self.is_over() and pygame.mouse.get_pressed()[0]:
                return True

    def constructor(self):
        self.display_surface.blit(
            self.button_img["top_left"], (self.position["x"], self.position["y"]))

        self.display_surface.blit(
            self.button_img["top_right"], (self.position["x"] + self.position["width"] - (self.button_img["top_right"].get_width() * 2), self.position["y"]))

        self.display_surface.blit(
            self.button_img["bottom_left"], (self.position["x"], self.position["y"] + self.position["height"] - (self.button_img["bottom_left"].get_height() * 2)))

        self.display_surface.blit(
            self.button_img["bottom_right"], (self.position["x"] + self.position["width"] - (self.button_img["bottom_right"].get_width() * 2), self.position["y"] + self.position["height"] - (self.button_img["bottom_right"].get_height() * 2)))

        self.display_surface.blit(
            pygame.transform.scale(self.button_img["bottom"], (self.position["width"] - (self.button_img["bottom_left"].get_width() * 3), self.button_img["bottom"].get_height())), (self.position["x"] + self.button_img["bottom_left"].get_width(), self.position["y"] + self.position["height"] - (self.button_img["bottom"].get_height() * 2)))

        self.display_surface.blit(
            pygame.transform.scale(self.button_img["top"], (self.position["width"] - (self.button_img["top_left"].get_width() * 3), self.button_img["top"].get_height())), (self.position["x"] + self.button_img["bottom_left"].get_width(), self.position["y"]))

        self.display_surface.blit(
            pygame.transform.scale(self.button_img["left"], (self.button_img["left"].get_width(), self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"], self.position["y"] + self.button_img["top_left"].get_height()))

        self.display_surface.blit(
            pygame.transform.scale(self.button_img["right"], (self.button_img["right"].get_width(), self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"] + self.position["width"] - (self.button_img["right"].get_width() * 2.5), self.position["y"] + self.button_img["top_right"].get_height()))

        if self.is_over():
            self.display_surface.blit(
                pygame.transform.scale(self.button_img["white"], (self.position["width"] - (self.button_img["top_left"].get_width() * 3), self.position["height"] - (self.button_img["top_left"].get_height() * 3) + (self.button_img["top_left"].get_height() / 3))), (self.position["x"] + self.button_img["top_left"].get_width(), self.position["y"] + (self.button_img["top_left"].get_height() * 2/3)))

            self.display_surface.blit(
                pygame.transform.scale(self.button_img["white"], (self.button_img["top_left"].get_width() / 3, self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"] + self.button_img["left"].get_width(), self.position["y"] + self.button_img["top_left"].get_height()))

            self.display_surface.blit(
                pygame.transform.scale(self.button_img["white"], (self.button_img["top_left"].get_width() / 3, self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"] + self.position["width"] - (self.button_img["top_right"].get_width() * 2), self.position["y"] + self.button_img["top_left"].get_height()))

        else:
            self.display_surface.blit(
                pygame.transform.scale(self.button_img["grey"], (self.position["width"] - (self.button_img["top_left"].get_width() * 3), self.position["height"] - (self.button_img["top_left"].get_height() * 3) + (self.button_img["top_left"].get_height() / 3))), (self.position["x"] + self.button_img["top_left"].get_width(), self.position["y"] + (self.button_img["top_left"].get_height() * 2/3)))

            self.display_surface.blit(
                pygame.transform.scale(self.button_img["grey"], (self.button_img["top_left"].get_width() / 3, self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"] + self.button_img["left"].get_width(), self.position["y"] + self.button_img["top_left"].get_height()))

            self.display_surface.blit(
                pygame.transform.scale(self.button_img["grey"], (self.button_img["top_left"].get_width() / 3, self.position["height"] - (self.button_img["top_left"].get_height() * 3))), (self.position["x"] + self.position["width"] - (self.button_img["top_right"].get_width() * 2), self.position["y"] + self.button_img["top_left"].get_height()))

    def update(self):
        self.constructor()
        self.my_text.draw()

        if not self.active:
            self.unactive_time -= 1
            if self.unactive_time <= 0:
                self.active = True
        else:
            if self.is_pressed() and self.action:
                return self.action
            else:
                return None
        return None

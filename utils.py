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
    def __init__(self, surface, str, size, pos, color=(0, 0, 0), max_with=1920):

        self.display_surface = surface

        self.pos = pos

        self.color = color

        self.text_image = {}

        self.line_width = {}

        self.spritesheet = Spritesheet(
            "mappeur_files/internal/text/spritesheet.png", (0, 0, 0), color)

        with open("mappeur_files/internal/text/spritesheet.json") as f:
            self.data = json.load(f)

        for cara in list(self.data["frames"].keys()):
            self.text_image[cara] = self.spritesheet.parse_sprite(cara)

        self.possible_cara = self.data["frames"].keys()

        self.text = str

        self.size = size

        if "\n" in self.text:
            self.text = self.text.split("\n")
        else:
            self.text = [self.text]

        for line in self.text:
            for cara in line:
                if cara not in self.possible_cara:
                    self.text = str.replace(cara, " None ")

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

    def get_height(self):
        return len(self.line_width) * 7 * self.size

    def get_width(self):
        return max(self.line_width.values())

    def draw(self):
        for line_nb, line in enumerate(self.text):
            self.pos_x = self.pos[0]
            for cara in line:
                self.display_surface.blit(pygame.transform.scale(self.text_image[cara], (self.text_image[cara].get_width(
                ) * self.size, self.text_image[cara].get_height() * self.size)), (self.pos_x, self.pos[1] + (7 * self.size * line_nb)))
                self.pos_x += self.text_image[cara].get_width() * self.size

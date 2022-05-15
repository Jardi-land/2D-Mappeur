import os.path
import pygame


def import_folder(path, name):
    surface_list = []
    surface_numb = 1

    while True:
        if os.path.exists(f"{path}/{name}{surface_numb}.png"):
            surface_list.append(pygame.image.load(
                f"{path}/{name}{surface_numb}.png").convert_alpha())
            surface_numb += 1
        else:
            break

    if surface_numb == 1:
        print("path doesn't exist")

    return surface_list

import os
import pygame
from settings import *
from interface import *

pygame.init()


def main():
    os.chdir(os.path.dirname(__file__))

    screen = pygame.display.set_mode((screen_res[0], screen_res[1]))
    pygame.display.set_caption(window_name)
    clock = pygame.time.Clock()

    interface = Interface(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw event here
        interface.draw()

        pygame.display.update()
        clock.tick(60)


main()

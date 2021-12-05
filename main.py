import sys, pygame
from settings import *

pygame.init()

def main():
    screen = pygame.display.set_mode((screen_res[0], screen_res[1]))
    pygame.display.set_caption(window_name)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw event here        

        pygame.display.update()
        clock.tick(60)

main()
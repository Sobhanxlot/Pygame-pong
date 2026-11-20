import pygame
import sys

screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Pygame Pong")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((222, 251, 194))

    pygame.display.update()
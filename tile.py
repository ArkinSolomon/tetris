import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, screen, width, x, y, color):
        super().__init__()

        self.screen = screen
        self.width = width
        self.x = x
        self.y = y
        self.color = color

        self.image = pygame.Surface([width - 1, width - 1])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

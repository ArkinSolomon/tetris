import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, screen, size, coords, color):
        super().__init__()

        self.screen = screen
        self.size = size
        self.x = coords[0]
        self.y = coords[1]
        self.color = color

        self.image = pygame.Surface([size - 1, size - 1])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

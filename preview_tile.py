import pygame

class Preview_Tile:

    def __init__(self, x, y, color, size, screen):
        self.x = x
        self.y = y
        self.color = color
        self.screen = screen
        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

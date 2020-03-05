import pygame
from tile import Tile
import random as r
from math import floor
from copy import deepcopy
import sys

class Block:

    def __init__(self, screen, tile_size, side_size, width, height, map, all_sprites):
        self.tile_group = pygame.sprite.Group()
        self.screen = screen
        self.tile_size = tile_size
        self.width = width
        self.heignt = height
        self.map = map
        self.all_sprites = all_sprites

        self.coords = None
        self.collide = False

        self.type = 0 #r.randrange(0, 6, 1)
        self.middle_tile_index = floor(width / 2) - 1
        self.middle_tile = (self.middle_tile_index * tile_size + (self.middle_tile_index + 1)) + side_size

        self.__generate()

    def draw(self):
        for tile in self.tile_group:
            pygame.draw.rect(self.screen, self.color, [tile.rect.x, tile.rect.y, self.tile_size - 1, self.tile_size - 1], 0)

    def update(self):
        old_coords = deepcopy(self.coords)
        for coord in self.coords:
            coord[0] += 1
            if self.map[coord[0]][coord[1]]:
                self.collide = True
                break
        for coord in old_coords:
            self.map[coord[0]][coord[1]] = False
        for coord in self.coords:
            self.map[coord[0]][coord[1]] = True
        for tile in self.tile_group:
            tile.rect.x += self.tile_size + 1

    def turn(self, dir):
        if dir == 'cw': pass
        elif dir == 'ccw': pass

    def __generate(self):
        if self.type == 0:
            self.color = pygame.Color('lightblue')

            self.map[0][self.middle_tile_index] = True
            self.map[1][self.middle_tile_index] = True
            self.map[2][self.middle_tile_index] = True
            self.map[3][self.middle_tile_index] = True

            # [y, x]
            self.coords = [[0, self.middle_tile_index], [1, self.middle_tile_index], [2, self.middle_tile_index], [3, self.middle_tile_index]]
            self.tile_group.add(Tile(self.screen, self.tile_size, self.middle_tile, 1, self.color))
            self.tile_group.add(Tile(self.screen, self.tile_size, self.middle_tile, 2 + self.tile_size, self.color))
            self.tile_group.add(Tile(self.screen, self.tile_size, self.middle_tile, 3 + self.tile_size * 2, self.color))
            self.tile_group.add(Tile(self.screen, self.tile_size, self.middle_tile, 4 + self.tile_size * 3, self.color))
            self.all_sprites.add(self.tile_group)
            pass

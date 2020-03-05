import pygame
from tile import Tile
import random as r
from math import floor
from copy import deepcopy
import sys

class Block:

    def __init__(self, screen, tile_size, side_size, width, height, map, all_sprites):
        self.screen = screen
        self.tile_size = tile_size
        self.side_size = side_size
        self.width = width
        self.heignt = height
        self.map = map
        self.all_sprites = all_sprites

        self.coords = None
        self.can_move = True

        self.type = 0 #r.randrange(0, 6, 1)
        self.middle_tile_index = floor(width / 2) - 1
        self.middle_tile = (self.middle_tile_index * tile_size + (self.middle_tile_index + 1)) + side_size

        self.__generate()

    def draw(self):
        for t in self.coords:
            tile = t[2]
            pygame.draw.rect(self.screen, self.color, [tile.rect.x, tile.rect.y, self.tile_size - 1, self.tile_size - 1], 0)

    def update(self, left, right, down):
        if not self.can_move: return
        collide = False
        test_map = deepcopy(self.map)
        for coord in self.coords:
            test_map[coord[0]][coord[1]] = False
        for coord in self.coords:
            if self.__check_collide(coord[0], coord[1] + 1):
                self.can_move = False
                collide = True
                break
        if not collide:
            for coord in self.coords:
                coord[1] += 1
                coord[2].rect.y = self.get_coords(coord[0], coord[1])[1]

    def get_coords(self, x, y):
        return [(x * self.tile_size) + self.side_size + x + 1, (y * self.tile_size) + y + 1]

    def __generate(self):
        if self.type == 0:
            if not self.__check_collide(self.middle_tile_index, 0) and not self.__check_collide(self.middle_tile_index, 1) and not self.__check_collide(self.middle_tile_index, 2) and not self.__check_collide(self.middle_tile_index, 3):
                self.color = pygame.Color('lightblue')
                self.coords = [[self.middle_tile_index, 0, Tile(self.screen, self.tile_size, self.get_coords(self.middle_tile_index, 0), self.color)], [self.middle_tile_index, 1, Tile(self.screen, self.tile_size, self.get_coords(self.middle_tile_index, 1), self.color)], [self.middle_tile_index, 2, Tile(self.screen, self.tile_size, self.get_coords(self.middle_tile_index, 2), self.color)], [self.middle_tile_index, 3, Tile(self.screen, self.tile_size, self.get_coords(self.middle_tile_index, 3), self.color)]]
                for t in self.coords: self.all_sprites.add(t[2])

    def __check_collide(self, ix, iy):
        if self.map[ix][iy]:
            return True

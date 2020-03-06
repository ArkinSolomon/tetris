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
        self.height = height
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
        exclusive_map = deepcopy(self.map)
        l = self.width
        r = -1
        for coord in self.coords:
            exclusive_map[coord[0]][coord[1]] = False
            if coord[1] < l:
                l = coord[1]
            if coord[1] > r:
                r = coord[1]
        for coord in self.coords:
            if self.__check_collide(coord[0], coord[1], map=exclusive_map):
                collide = True
                break
        if not collide:
            for coord in self.coords:
                exclusive_map[coord[0]][coord[1]] = False
                coord[0] += 1
                if down: coord[0] += 1
                if left and coord[1] > l: coord[1] -= 1
                if right and coord[1] < r: coord[1] += 1
                exclusive_map[coord[0]][coord[1]] = False
                coord[2].rect.y, coord[2].rect.x = self.get_coords(coord[0], coord[1])
        else:
            self.can_move = False

    def get_coords(self, y, x):
        return ((y * self.tile_size) + y + 1, (x * self.tile_size) + self.side_size + x + 1)

    def __generate(self):
        if self.type == 0:
            if not self.__check_collide(0, self.middle_tile_index) and not self.__check_collide(1, self.middle_tile_index) and not self.__check_collide(2, self.middle_tile_index) and not self.__check_collide(3, self.middle_tile_index):
                self.color = pygame.Color('lightblue')
                self.coords = [[0, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(0, self.middle_tile_index), self.color)], [1, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(1, self.middle_tile_index), self.color)], [2, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(2, self.middle_tile_index), self.color)], [3, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(3, self.middle_tile_index), self.color)]]
                for t in self.coords: self.all_sprites.add(t[2])

    def __check_collide(self, iy, ix, map=None):
        if map is None:
            if self.map[iy][ix] or iy >= self.height - 1:
                return True
        else:
            if map[iy][ix] or iy >= self.height - 1:
                return True
        return False

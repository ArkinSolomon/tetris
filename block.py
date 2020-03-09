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
        self.axis = None
        self.can_move = True

        self.updates = 0
        self.update_every = 5

        self.type = 0 #r.randrange(0, 6, 1)
        self.middle_tile_index = floor(width / 2) - 1
        self.middle_tile = (self.middle_tile_index * tile_size + (self.middle_tile_index + 1)) + side_size

        self.generate()

    def draw(self):
        for t in self.coords:
            tile = t[2]
            if not tile.draw: continue
            pygame.draw.rect(self.screen, self.color, [tile.rect.x, tile.rect.y, self.tile_size - 1, self.tile_size - 1], 0)

    def turn(self, dir):
        if dir == 'cw':
            collide = False
            exclusive_map = deepcopy(self.map)
            for coord in self.coords:
                exclusive_map[coord[0]][coord[1]] = False
            for coord in self.coords:
                if coord[2] == self.coords[self.axis][2]: continue
                dist_from_axis_x = coord[1] - self.coords[self.axis][1]
                dist_from_axis_y = coord[0] - self.coords[self.axis][0]
                if self.__check_collide(self.coords[self.axis][0] + dist_from_axis_x * -1, self.coords[self.axis][1] + dist_from_axis_y, map=exclusive_map):
                    collide = True
                    break
            if not collide:
                for coord in self.coords: self.map[coord[0]][coord[1]] = False
                for coord in self.coords:
                    if coord[2] == self.coords[self.axis][2]: continue
                    dist_from_axis_x = coord[1] - self.coords[self.axis][1]
                    dist_from_axis_y = coord[0] - self.coords[self.axis][0]
                    coord[0] = self.coords[self.axis][0] + dist_from_axis_x * -1
                    coord[1] = self.coords[self.axis][1] + dist_from_axis_y
                    coord[2].rect.y, coord[2].rect.x = self.get_coords(coord[0], coord[1])
        elif dir == 'ccw': pass

    def update(self, left, right):
        if not self.can_move: return
        self.updates += 1
        update = self.updates >= self.update_every
        collide = False
        side_collide = False
        exclusive_map = deepcopy(self.map)
        for coord in self.coords:
            exclusive_map[coord[0]][coord[1]] = False
        for coord in self.coords:
            if update:
                if self.__check_collide(coord[0] + 1, coord[1], map=exclusive_map):
                    collide = True
                    break
                if left and self.__check_collide(coord[0] + 1, coord[1] - 1, map=exclusive_map): side_collide = True
                if right and self.__check_collide(coord[0] + 1, coord[1] + 1, map=exclusive_map): side_collide = True
            else:
                if left and self.__check_collide(coord[0], coord[1] - 1, map=exclusive_map): side_collide = True
                if right and self.__check_collide(coord[0], coord[1] + 1, map=exclusive_map): side_collide = True
        if not collide:
            for coord in self.coords: self.map[coord[0]][coord[1]] = False
            for coord in self.coords:
                if update: coord[0] += 1
                if left and not side_collide: coord[1] -= 1
                if right and not side_collide: coord[1] += 1
                self.map[coord[0]][coord[1]] = True
                coord[2].rect.y, coord[2].rect.x = self.get_coords(coord[0], coord[1])
                if not collide or not side_collide:
                    coord[2].map_coord_x = coord[1]
                    coord[2].map_coord_y = coord[0]
            if update: self.updates = 0
        else:
            self.can_move = False

    def get_coords(self, y, x):
        return ((y * self.tile_size) + y + 1, (x * self.tile_size) + self.side_size + x + 1)

    def generate(self):
        if self.type == 0:
            if not self.__check_collide(0, self.middle_tile_index) and not self.__check_collide(1, self.middle_tile_index) and not self.__check_collide(2, self.middle_tile_index) and not self.__check_collide(3, self.middle_tile_index):
                self.color = pygame.Color('lightblue')
                self.coords = [[0, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(0, self.middle_tile_index), self.color)], [1, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(1, self.middle_tile_index), self.color)], [2, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(2, self.middle_tile_index), self.color)], [3, self.middle_tile_index, Tile(self.screen, self.tile_size, self.get_coords(3, self.middle_tile_index), self.color)]]
                self.axis = 1
                for coord in self.coords:
                    self.map[coord[0]][coord[1]] = True
                    self.all_sprites.add(coord[2])
            else: return True

    def __check_collide(self, iy, ix, map=None):
        if ix >= self.width or ix < 0: return True
        if map is None:
            try:
                self.map[iy][ix]
            except: return True
            if self.map[iy][ix] or iy > self.height - 1:
                return True
        else:
            try:
                map[iy][ix]
            except: return True
            if map[iy][ix] or iy > self.height - 1:
                return True
        return False

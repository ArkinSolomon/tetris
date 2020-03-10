import pygame
from block import Block
import numpy as np
import sys
import os

def clear():
    if sys.platform == 'win32':
        os.system('cls')
    else: os.system('clear')

clear()

width = 9
height = 20
tile_size = 35
side_size = 300
border_color = pygame.Color('#dbdbdb')
current_border_color = pygame.Color('#dbc21f')
print_data = '--print-data' in sys.argv

if '-w' in sys.argv:
    width = int(sys.argv[sys.argv.index('-w') + 1])
if '--width' in sys.argv:
    width = int(sys.argv[sys.argv.index('--width') + 1])
if '-h' in sys.argv:
    height = int(sys.argv[sys.argv.index('-h') + 1])
if '--height' in sys.argv:
    height = int(sys.argv[sys.argv.index('--height') + 1])

def get_coords(y, x):
    return ((y * tile_size) + y + 1, (x * tile_size) + side_size + x + 1)

pygame.init()
screen_x = (width * tile_size + width) + (side_size * 2)
screen_y = (height * tile_size) + height
screen = pygame.display.set_mode([screen_x, screen_y], pygame.HWSURFACE)
pygame.display.set_caption('Tetris')

pygame.key.set_repeat(300)

map = np.zeros((height, width), dtype=np.bool)

tiles = []
x = side_size
y = 0
for _ in range(width):
    for _ in range(height):
        tiles.append(pygame.Rect(x, y, tile_size, tile_size))
        y += tile_size + 1
    x += tile_size + 1
    y = 0

all_sprites = pygame.sprite.Group()

current_block = Block(screen, tile_size, side_size, width, height, map, all_sprites)
next_block = Block(screen, tile_size, side_size, width, height, map, all_sprites)

blocks = []

game_is_active = True

clock = pygame.time.Clock()

while game_is_active:

    keys = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_active = False
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys.append('left')
            if event.key == pygame.K_RIGHT:
                keys.append('right')
            if event.key == pygame.K_DOWN:
                keys.append('down')
            if event.key == pygame.K_UP:
                keys.append('up')

    screen.fill((0, 0, 0))

    for tile in tiles:
        pygame.draw.lines(screen, border_color, True, [(tile.x, tile.y), (tile.right, tile.y), (tile.right, tile.bottom), (tile.x, tile.bottom)])

    if 'down' in keys and not 'up' in keys:
        current_block.turn('cw')
    if 'up' in keys and not 'down' in keys:
        current_block.turn('ccw')

    current_block.update('left' in keys, 'right' in keys)
    for t in current_block.coords:
        tile = t[2].rect
        pygame.draw.lines(screen, current_border_color, True, [(tile.x, tile.y), (tile.right, tile.y), (tile.right, tile.bottom), (tile.x, tile.bottom)])
    if not current_block.can_move:
        for coord in current_block.coords:
            if coord[0] <= 0:
                print('You lost :(')
                game_is_active = False
                break
        blocks.append(current_block)
        current_block = next_block
        for i in range(len(map)):
            row = map[i]
            if not (False in row):
                for j in range(len(row)):
                    for tile in all_sprites:
                        if tile.map_coord_y == i and tile.map_coord_x == j:
                            all_sprites.remove(tile)
                            tile.draw = False
                for j in range(len(row)): row[j] = False
                tiles_to_drop = []
                for tile in all_sprites:
                    if tile.map_coord_y < i:
                        map[tile.map_coord_y][tile.map_coord_x] = False
                        tiles_to_drop.append(tile)
                for tile in tiles_to_drop:
                    tile.map_coord_y += 1
                    tile.rect.y, tile.rect.x = get_coords(tile.map_coord_y, tile.map_coord_x)
                    map[tile.map_coord_y][tile.map_coord_x] = True
        if current_block.generate() and game_is_active:
            print('You lost :(')
            game_is_active = False
            break
        next_block = Block(screen, tile_size, side_size, width, height, map, all_sprites)

    for block in blocks: block.draw()
    current_block.draw()

    pygame.display.flip()

    if print_data:
        clear()
        print(map)
        print('LEFT:', 'left' in keys)
        print('RIGHT:', 'right' in keys)
        print('UP:', 'up' in keys)
        print('DOWN:', 'down' in keys)
        print('UPDATES:', current_block.updates)
        print('TYPE:', current_block.type)
        print('COORDS:', current_block.coords)

    clock.tick(60)

sys.exit(0)

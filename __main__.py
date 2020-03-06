import pygame
from block import Block
import numpy as np
import sys

width = 10
height = 20
tile_size = 35
side_size = 300
border_color = pygame.Color('#dbdbdb')

if '-w' in sys.argv:
    width = int(sys.argv[sys.argv.index('-w') + 1])
if '--width' in sys.argv:
    width = int(sys.argv[sys.argv.index('--width') + 1])
if '-h' in sys.argv:
    height = int(sys.argv[sys.argv.index('-h') + 1])
if '--height' in sys.argv:
    height = int(sys.argv[sys.argv.index('--height') + 1])

pygame.init()
screen_x = (width * tile_size + width) + (side_size * 2)
screen_y = (height * tile_size) + height
screen = pygame.display.set_mode([screen_x, screen_y], pygame.HWSURFACE)
pygame.display.set_caption('Tetris')

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_active = False
            sys.exit(0)

    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    for tile in tiles:
        pygame.draw.lines(screen, border_color, True, [(tile.x, tile.y), (tile.right, tile.y), (tile.right, tile.bottom), (tile.x, tile.bottom)])

    current_block.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_SPACE])
    if not current_block.can_move:
        blocks.append(current_block)
        current_block = next_block
        next_block = Block(screen, tile_size, side_size, width, height, map, all_sprites)

    for block in blocks: block.draw()
    current_block.draw()    

    pygame.display.flip()

    clock.tick(2)

sys.exit(0)

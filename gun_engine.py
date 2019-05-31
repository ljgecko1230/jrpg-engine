import pygame, sys, time, random, math
from PIL import Image

pygame.init()

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_move = True
        self.is_moving = "down"
    def update(self):
        self.top = self.y
        self.bottom = self.y + tile_size
        self.left = self.x
        self.right = self.x + tile_size

screen = pygame.display.set_mode((800, 600))
tile_size = 45
camera_x = 0
camera_y = 0
rendered_image = Image.new("RGB", (2000, 2000))
tall_grass = Image.open("tall_grass.png")
stone_pathway = Image.open("stone_pathway.png")

with open("level.txt") as file:
    creation_x = 0
    creation_y = 0
    for line in file:
        creation_x = 0
        for character in line:
            if character == "t":
                new_tile = tall_grass.crop((0, 0, tile_size, tile_size))
                rendered_image.paste(new_tile, (creation_x, creation_y, creation_x + tile_size, creation_y + tile_size))
            elif character == "p":
                new_tile = stone_pathway.crop((0, 0, tile_size, tile_size))
                rendered_image.paste(new_tile, (creation_x, creation_y, creation_x + tile_size, creation_y + tile_size))
            elif character == "!":
                offset_x = int(400 - (tile_size / 2) - creation_x)
                offset_y = int(300 - (tile_size / 2) - creation_y) 
                camera_offset_x = creation_x
                camera_offset_y = creation_y
                rendered_image.paste(new_tile, (creation_x, creation_y, creation_x + tile_size, creation_y + tile_size))
                player = Player(creation_x + offset_x, creation_y + offset_y)
            creation_x += tile_size
        creation_y += tile_size

rendered_image.save("rendered_image.png")
rendered_image = pygame.image.load("rendered_image.png")
camera_x = player.x - camera_offset_x
camera_y = player.y - camera_offset_y
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    screen.fill((0, 0, 0))
    
    player.update()
    
    if player.can_move == True:
        if pygame.key.get_pressed()[pygame.K_RIGHT]: 
            player.can_move = False
            player.is_moving = "right"
            moves = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.can_move = False
            player.is_moving = "left"
            moves = 0
        if pygame.key.get_pressed()[pygame.K_UP]:
            player.can_move = False
            player.is_moving = "up"
            moves = 0
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player.can_move = False
            player.is_moving = "down"
            moves = 0
    elif player.can_move == False:
        if moves < tile_size:
            if player.is_moving == "right":
                moves += 1
                camera_x -= 1
            elif player.is_moving == "left":
                moves += 1
                camera_x += 1
            elif player.is_moving == "up":
                moves += 1
                camera_y += 1
            elif player.is_moving == "down":
                moves += 1
                camera_y -= 1
        else:
            player.can_move = True
    
    screen.blit(rendered_image, (camera_x, camera_y))
    screen.blit(pygame.image.load("stone_pathway.png"), (player.x, player.y))
    
    pygame.display.flip()

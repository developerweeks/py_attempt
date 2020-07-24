# draw the village

import pygame

# initialize
pygame.init()

# create a screen that is x by y
screen = pygame.display.set_mode((800,600))
# screen will go away when script reaches the end
# top left of screen is (0,0) and bottom left is (0,600)

#title and icon
pygame.display.set_caption('The village')
icon = pygame.image.load('forest.png')
pygame.display.set_icon(icon)

# first object
playerImg = pygame.image.load('menhir.png')
playerX = 370
playerY = 480
# position of the top left corner of the image

def player():
    screen.blit(playerImg, (playerX, playerY))
    # blit means to draw

# main game loop
running = True
while running:
    screen.fill((171, 205, 239))
    # every key press is an event
    for event in pygame.event.get():
        if event.type == pygame.quit():
            running = False

    # draw the player after filling the screen, so it is drawn on top
    player()

    pygame.display.update()
    pygame.time.delay(5)


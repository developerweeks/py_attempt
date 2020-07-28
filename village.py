# draw the village
import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

screenWidth = 400
screenHeight = 300
# create a screen that is x by y
screen = pygame.display.set_mode((2*screenWidth,2*screenHeight))
# screen will go away when script reaches the end
# top left of screen is (0,0) and bottom left is (0,600)


# Sound
#mixer.music.load("zelda_chill.wav")
#mixer.music.play(-1)

# title and icon
pygame.display.set_caption('The village')
icon = pygame.image.load('forest.png')
pygame.display.set_icon(icon)

# first object
viewpointX = 0
viewpointY = 0
viewpointStep = 1
viewslide = {'x': 0, 'y': 0}
# the viewpoint can be manipluated with arrow keys

fieldTypes = [
    pygame.image.load('crop.png'), 
    pygame.image.load('forest.png'), 
    pygame.image.load('menhir.png')]

# village tile collection
tileX = [] # left-right
tileY = [] # up-down
tileZ = [] # type
tileCount = 8
Tselected = False

# range is 0-indexed
for i in range(tileCount):
    tileX.append(random.randint(200, 600))
    tileY.append(random.randint(100, 500))
    tileZ.append(i%len(fieldTypes))


# HUD
font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

# helper functions
def show_score(x, y):
    score = font.render("Scale : " + str(tileCount), True, (255, 255, 255))
    screen.blit(score, (x, y))
    # blit means to draw

def swrite(line, x, y):
    words = font.render(str(line), True, (255, 255, 255))
    screen.blit(words, (x, y))
    # blit means to draw

def tile(x, y, i):
    z = tileZ[i]
    screen.blit(fieldTypes[z], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 15:   # pixel radius of tile image
        return True
    else:
        return False



# main game loop
running = True
while running:
    # solid background color, we draw this first so other things go on top
    screen.fill((171, 205, 239))
    # Background Image
    #screen.blit(background, (0, 0))

    # every key press is an event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, respond
        # wow this list is getting really long
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_x, pygame.K_v, pygame.K_SPACE]:
                print(event.key)
            if event.key == pygame.K_q:
                running = False
            #print(event.key)
            # moving the screen
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                viewslide['x'] = viewpointStep
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                viewslide['x'] = 0 - viewpointStep
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                viewslide['y'] = 0 - viewpointStep
            if event.key in [pygame.K_UP, pygame.K_w]:
                viewslide['y'] = viewpointStep
            # recenter
            if event.key == pygame.K_LCTRL:
                viewpointX = 0
                viewpointY = 0
            # change movement speed
            if event.key == pygame.K_PLUS:
                viewpointStep = viewpointStep + 1
            if event.key == pygame.K_MINUS:
                viewpointStep = viewpointStep - 1
            # select a tile and open them menu
            if event.key == pygame.K_SPACE:
                print('which? '+ str(viewpointX) +' '+ str(viewpointY))
                # select the tile currently viewed at (screenWidth, screenHeight)
                for i in range(tileCount):
                    tx = tileX[i]+viewpointX
                    ty = tileY[i]+viewpointY
                    collision = isCollision(tx, ty, screenWidth, screenHeight)
                    if collision:
                        Tselected = i
                        print(i)

            # the menu parts for the selected tile
            if event.key == pygame.K_x:
                Tselected = 'x'
                # exit the menu
            # actions on the tile require a title be selected
            if type(Tselected) == 'int':
                if event.key == pygame.K_v:
                    tx = tileX[Tselected] = screenWidth - viewpointX
                    ty = tileY[Tselected] = screenHeight - viewpointY

        if type(Tselected) == 'int':
            # sometile is selected, keep the options open
            tx = tileX[Tselected]+viewpointX
            ty = tileY[Tselected]+viewpointY
            ttype = tileZ[Tselected]
            screen.blit(pygame.image.load('focus.png'), (tx, ty))
            swrite('x: close menu', 30, 45)
            swrite('v: move', 30, 80)
            swrite('f: fortify', 30, 115)
            if tileZ[Tselected] == 0:
                # a crop/pasture field
                swrite('e: train', 30, 150)



        if event.type == pygame.KEYUP:
            viewslide = {'x': 0, 'y': 0}
            # continuous movement when the button was held down
            # stop movement when the button is released

    # shift viewer's center
    viewpointX = viewpointX + viewslide['x']
    viewpointY = viewpointY + viewslide['y']

    # bounds checking
    if viewpointX <= -screenWidth:
        viewpointX = -screenWidth
    elif viewpointX >= screenWidth:
        viewpointX = screenWidth

    if viewpointY <= -screenHeight:
        viewpointY = -screenHeight
    elif viewpointY >= screenHeight:
        viewpointY = screenHeight

    # tile reposition
    for i in range(tileCount):
        # tile blit
        tx = tileX[i]+viewpointX
        ty = tileY[i]+viewpointY
        tile(tx, ty, tileZ[i])


        # Selection
        collision = isCollision(tx, ty, screenWidth, screenHeight)
        if collision:
            # show selector
            screen.blit(pygame.image.load('focus.png'), (screenWidth, screenHeight))
        #    explosionSound = mixer.Sound("explosion.wav")
        #    explosionSound.play()

    show_score(textX, textY)
    pygame.display.update()


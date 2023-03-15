#########################################
# Programmer: Matthew Bodenstein
# Date: 05/16/2019
# File Name: tetris_template3.py
# Description: This program is the third game template for our Tetris game.
#########################################
import pygame
HEIGHT = 600          # height of the screen/display
WIDTH  = 800          # width of the screen/display
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))   # sets screen above importing tetris so images work properly
from tetris_classes3 import *
from random import randint
import time
pygame.init()

pygame.mixer_music.load("TETRISSONG.ogg")    # plays music
pygame.mixer_music.set_volume(0.2)           #
pygame.mixer_music.play(-1)                  #
tetris = 0      # adds 1 every tetris to be counted for back to back tetris
lvl2 = False        # different levels
lvl3 = False
pause = False#
pauseWait = 100
inPlay = False
start = True
swap = False
end = False
GREY = (192,192,192)
backround = pygame.image.load("backroundTet.jpg")           # sets all the backrounds
backround = backround.convert_alpha()                       #
backroundend = pygame.image.load("backroundend.jpg")        #
backroundend = backroundend.convert_alpha()                 #
backroundstart = pygame.image.load("backroundstart.jpg")    #
backroundstart = backroundstart.convert_alpha()             #
score = 0 # sets score
speed = 0 # sets speed of shape
level = 0 # sets level
elapseTime=0        # Timer variables/propertiest
endTime=0           #
font = pygame.font.SysFont("Ariel Black", 75)  # create a variable font
time_started = False  # if time is started then the timer will start counting
#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = 1                                 #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen(score):
    time1 = font.render(str(elapseTime), 1, RED)  # printing time
    text = font.render(str(score), 1, RED)  # put the font and the message together      #
    text2 = font.render(str(level), 1, RED)
    screen.blit(backround, (0,0))
    shape.draw(screen, GRIDSIZE)    # draws the shape
    floor.draw(screen, GRIDSIZE)    # draws the floor
    leftWall.draw(screen, GRIDSIZE) # draws left wall
    rightWall.draw(screen, GRIDSIZE)# draws right wall
    obstacles.draw(screen, GRIDSIZE)
    pygame.draw.rect(screen, WHITE, (20, 120, 150,150))    # Draw the boarder of the place that shows the upcoming blocks
    pygame.draw.rect(screen, BLACK, (30, 130, 130, 130))   # Draws the inside of the place showing the upcoming blocks
    pygame.draw.rect(screen, WHITE, (20, 120+250, 150, 150))  # Draw the boarder of the place that shows the hold blocks
    pygame.draw.rect(screen, BLACK, (30, 130+250, 130, 130))  # Draws the inside of the place showing the hold blocks
    shadow.draw(screen, GRIDSIZE)   # draws shadow
    txt("TETRIS", 100, 50, 100, RED)    #
    txt("HOLD", 100, 50+250, 100, RED)  # all of the text displayed
    txt("SCORE", 700, 50, 100, RED)     #
    txt("LEVEL", 700, 225, 100, RED)    #
    txt("TIME", 700, 400, 100, RED)     #
    hold.draw(screen, GRIDSIZE)
    screen.blit(text2, (675, 300))
    screen.blit(text, (675, 120))   # draw it on the screen at the text_X and text_Y      #
    screen.blit(time1, (675, 450))  # time being displayed on screen
    nextshape.draw(screen, GRIDSIZE)# next shape being displayed on screen
    pygame.display.update()

def start_screen():
    screen.blit(backroundstart, (0, 0))
    txt("TETRIS", 400, 50, 200, RED)
    txt("CLICK SPACE TO START", 400, 250, 150, RED)
    txt("PRESS C TO HOLD", 400, 450, 150, RED)
    pygame.display.update()

def end_screen():
    screen.blit(backroundend, (0, 0))
    txt("GAME OVER", 400 , 50, 200, RED)
    txt("SCORE", 400, 300, 100, RED)     #
    text = font.render(str(score), 1, RED)  # put the font and the message together
    screen.blit(text, (400, 350))   # draw it on the screen at the text_X and text_Y
    if time_started == True:
        endTime = time.time()  #
        elapseTime = endTime - startTime  # Pauses the time for end screen
        elapseTime = int(elapseTime)  #

def text_objects(text,font,colour):
    textSurface = font.render(text,True,colour)
    return textSurface, textSurface.get_rect()

def txt(text,x,y,size,colour):     # custom text function with custom font
    largeText = pygame.font.Font("RODAMAS.otf",size)
    TextSurf, TextRect = text_objects(text,largeText,colour)
    TextRect.center = (x,y)
    screen.blit(TextSurf,TextRect)
    pygame.display.update()

def shold(shape, hold, swap):
    temp = shape.clr
    shape.clr = hold.clr
    hold.clr = temp
    hold._rotate()
    swap = True
    shape.col = MIDDLE
    shape.row = TOP
    shape._rotate()
    return swap


#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)          # generates random shape number
newshapeNo = randint(1,7)
nextshape = Shape(LEFT-6,TOP + 6,newshapeNo)  # shows where the next shape will spawn
shape = Shape(MIDDLE,TOP,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)       #
leftWall = Wall(LEFT-1, TOP, ROWS)      # boundaries
rightWall = Wall(RIGHT, TOP, ROWS)      #
obstacles = Obstacles(LEFT, FLOOR)      #
ceiling = Floor(LEFT,TOP,COLUMNS)  #
hold = Shape(LEFT-6,TOP+16,5)


while start:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        start_screen()
        if keys[pygame.K_SPACE]:
            start = False
            inPlay = True
            startTime = time.time()

while inPlay:   # when game is in play

    if start == False and inPlay == True:  # keeps time running
        time_started = True
        endTime = time.time()  #
        elapseTime = endTime - startTime  # Calculating the elapse time
        elapseTime = int(elapseTime)  #

    keys = pygame.key.get_pressed()

    shadow = Shadow(shape.col, shape.row, shape.clr, shape._rot)  # this creates le shadow
    shadow._colOffsets = shape._colOffsets
    shadow._rowOffsets = shape._rowOffsets
    if shadow.drop(floor, obstacles):  # drops the shadow until it hits an object
        shadow.move_up()
    if score >= 0 and score < 500:
        speed = 120
        level = 1
        lvl2 = True
    elif score >= 500 and score < 1000:
        speed = 100
        level = 2
        lvl3 = True
        if lvl2 == True:
            a = pygame.mixer.Sound("lvlup.wav")
            a.play(0)
            lvl2 = False
    else:
        speed = 80
        level = 3
        if lvl3 == True:
            a = pygame.mixer.Sound("lvlup.wav")
            a.play(0)
            lvl3 = False
    redraw_screen(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                shape.rotateClkwise()
                shadow.rotateClk(floor, obstacles)

                if shape.collides(floor) or shape.collides(obstacles) or shape.collides(leftWall) or shape.collides(rightWall):
                    shape.rotateCntclkwise()


            if event.key == pygame.K_LEFT:
                shape.move_left()
                if shape.collides(leftWall) or shape.collides(obstacles):
                    shape.move_right()
            if event.key == pygame.K_RIGHT:
                shape.move_right()
                if shape.collides(rightWall) or shape.collides(obstacles):
                    shape.move_left()
            if event.key == pygame.K_SPACE:


                while not (shape.collides(floor) or shape.collides(obstacles)):
                    shape.move_down()
                shape.move_up()
                obstacles.append(shape)
                fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                #print("full rows", fullRows)
                score += obstacles.removeFullRows(fullRows, score, tetris)
                print(score)
                shape = Shape(MIDDLE, TOP, newshapeNo)
                newshapeNo= randint(1,7) # creates new shape
                nextshape = Shape(LEFT-6, TOP + 6, newshapeNo)
                a = pygame.mixer.Sound("place.wav")
                a.play(0)
                swap = False

    shape.move_down()
    if shape.collides(floor) or shape.collides(obstacles):
        a = pygame.mixer.Sound("place.wav")      # plays the placing sound
        swap = False
        a.play(0)                                #
        shape.move_up()
        obstacles.append(shape)
        fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
        print(score)   # prints score in terminal
        score += obstacles.removeFullRows(fullRows, score, tetris)   # adds score
        shape = Shape(MIDDLE, TOP, newshapeNo)
        newshapeNo = randint(1, 7)              # creates new shape
        nextshape = Shape(LEFT - 6, TOP + 6, newshapeNo)
    if obstacles.collides(ceiling):
        end = True
        t = pygame.mixer.Sound("death.wav")   # plays the death sound
        t.play(0)                             #
        inPlay = False       # breaks out by setting in play to false

    if keys[pygame.K_c] and swap == False:
        swap = shold(shape, hold, swap)

    pygame.display.update()
    pygame.time.delay(speed)

while end == True:
    end_screen()
    pygame.display.update()
    pygame.time.delay(2000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
pygame.quit()
    
    

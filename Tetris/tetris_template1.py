#########################################
# Programmer: Matthew Bodenstein
# Date: 05/9/2019
# File Name: tetris_template1.py
# Description: This program is the first game template for a Tetris game.
#########################################
from random import randint
from tetrisclasses import *
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
#Grid X layer
gridx_thic = 1
gridx_startx = 175
gridx_starty = 0+ 25
gridx_endx = GRIDSIZE * 14 +175
gridx_endy = 0+ 25
#Grid Y layer
gridy_thic = 1
gridy_startx = 175
gridy_starty = 0 + 25
gridy_endx = 175
gridy_endy = GRIDSIZE * 22 + 25

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen():               
    screen.fill(BLACK)
    draw_grid()
    shape.draw(screen, GRIDSIZE)
    pygame.display.update()

def draw_grid():
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    s1 = gridx_starty
    e1 = gridx_endy
    s2 = gridy_startx
    e2 = gridy_endx
    for i in range(23):
        pygame.draw.line(screen, WHITE, (gridx_startx, s1), (gridx_endx, e1), gridx_thic)
        s1 += GRIDSIZE
        e1 += GRIDSIZE
    for i in range(15):
        pygame.draw.line(screen, WHITE, (s2, gridy_starty), (e2, gridy_endy), gridy_thic)
        s2 += GRIDSIZE
        e2 += GRIDSIZE
    pygame.display.update()             # display must be updated, in order

#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)      
shape = Shape(1,1,shapeNo)
inPlay = True                                         

while inPlay:               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shape.move_up()
            if event.key == pygame.K_LEFT:
                shape.move_left()
            if event.key == pygame.K_RIGHT:
                shape.move_right()
            if event.key == pygame.K_DOWN:
                shape.move_down()
            if event.key == pygame.K_RSHIFT:
                shape.rot = (shape.rot + 1)%4
                shape.rotate()
            if event.key == pygame.K_SPACE:
                shape.clr = (shape.clr +1)%7 +1
                shape.rotate() # after changing the shape/clr the shape must be rotated and updated

# update the screen     
    redraw_screen()
    pygame.time.delay(30)
    
pygame.quit()
    
    

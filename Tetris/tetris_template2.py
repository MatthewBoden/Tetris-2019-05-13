###########################################################
# Programmer: Matthew Bodenstein
# Date: 05/15/2019
# File Name: tetris_template2.py
# Description: This program is the second game template for Tetris game.
############################################################
from tetris_classes2 import *
from random import randint
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#---------------------------------------#
COLUMNS: int = 14                       #
ROWS = 22                               #   LEARN WHAT... game field parameters are declared
LEFT = 9                                #   They determine where the grid section will be located.
TOP  = 1                                #
MIDDLE = LEFT + COLUMNS//2              #
FLOOR = TOP + ROWS                      #
RIGHT  = LEFT + COLUMNS                 #
Top = 0                                 #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen():               
    screen.fill(BLACK)
    shape.draw(screen, GRIDSIZE)
    floor.draw(screen, GRIDSIZE)
    wall.draw(screen, GRIDSIZE)
    wall2.draw(screen, GRIDSIZE)
    pygame.display.update() 
    
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)
#LEARN HOW TO... generate new shape objects based on the __init__ methood
shape = Shape(MIDDLE,TOP,shapeNo)

floor = Floor(LEFT,FLOOR,COLUMNS)
wall = Wall(RIGHT,Top+1,ROWS)
wall2 = Wall(LEFT-1,Top+1,ROWS)

inPlay = True                                         

while inPlay:               

    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shape.rot = (shape.rot + 1)%4     # 4 possible values for rotation - 0,1,2,3
                shape.rotate()

            if event.key == pygame.K_LEFT:
                shape.move_left()
                if shape.collides(wall2):
                    shape.move_right()

            if event.key == pygame.K_RIGHT:
                shape.move_right()
                if shape.collides(wall):
                    shape.move_left()

            if event.key == pygame.K_DOWN:
                shape.move_down()
                if shape.collides(floor):
                    shape.move_up()        

            if event.key == pygame.K_SPACE:
                shape.clr = shape.clr + 1
                if shape.clr > 7:
                    shape.clr = 1
                shape.rotate()

# update the screen     
    redraw_screen()
    pygame.time.delay(30)
    
pygame.quit()
    
    

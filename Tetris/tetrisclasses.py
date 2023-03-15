#########################################
# Programmer: Matthew Bodenstein
# Date: 05/9/2019
# File Name: tetris_classes1.py
# Description: These classes are templates for writing a Tetris game.
#########################################
import pygame

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
FIGURES   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]


class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface, WHITE, (x, y, gridsize, gridsize), 1)


    def move_left(self):                
        self.col = self.col - 1    
        
    def move_right(self):
        self.col = self.col + 1

    def move_down(self):
        self.row = self.row + 1

    def move_up(self):
        self.row = self.row - 1

#---------------------------------------#
class Shape(object):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
        auxiliary data:
            colOffsets - list of horizontal offsets for each block, in reference to the anchor block
            rowOffsets - list of vertical offsets for each block, in reference to the anchor block
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col         
        self.row = row
        self.clr = clr    
        self.rot = 1
        self.blocks = [Block()]*4        
        self.colOffsets = [-1, 0, 0, 1] 
        self.rowOffsets = [-1,-1, 0, 0] 
        self.rotate()
        
    def __str__(self):                  
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]
    
    def rotate(self):
        """ offsets are assigned starting from the farthest block in reference to the anchor block """

#####################################################################################################

        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            colOffsets = [[-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, -1]]
            rowOffsets = [[1, 0, 0, -1], [-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0]]

#####################################################################################################

        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]]
            rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]]

#####################################################################################################

        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o

            colOffsets = [[-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0], [1, 1, 0, -1]]
            rowOffsets = [[1, 1, 0, -1], [-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0]]

#####################################################################################################
        elif self.clr == 4:  #
                             #   o                o           o o
                             #   x            o x o             x           o x o
                             #   o o                            o           o

            colOffsets = [[1, 0, 0, 0], [-1,-1, 0, 1], [ -1, 0, 0, 0], [ 1, 1, 0,-1]]
            rowOffsets = [[ 1, 1, 0,-1], [1, 0, 0, 0], [-1,-1, 0, 1], [ -1, 0, 0, 0]]

#####################################################################################################

        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o
            colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]]
            rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]]

#####################################################################################################
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]]
            rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]]

#####################################################################################################

        elif self.clr == 7:  #
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]]
            rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]]


        self.colOffsets = colOffsets[self.rot]
        self.rowOffsets = rowOffsets[self.rot]
        self.update()
        
    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def move_left(self):                
        self.col = self.col - 1
        self.update()
        
    def move_right(self):               
        self.col = self.col + 1
        self.update()
        
    def move_down(self):                
        self.row = self.row + 1
        self.update()
        
    def move_up(self):                  
        self.row = self.row - 1
        self.update()
            
    def update(self):  # recaclulates all the offsets and create blocks wiht the new attributes
        for i in range(len(self.blocks)):
            blockCOL = self.col+self.colOffsets[i]
            blockROW = self.row+self.rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)
                                      


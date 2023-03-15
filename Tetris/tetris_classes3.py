#########################################
# Programmer: Matthew Bodenstein
# Date: 21/11/2015
# File Name: tetris_classes5.py
# Description: These classes are templates for writing a Tetris game.
#########################################
import pygame
o = pygame.image.load("0.jpg")
o = pygame.transform.scale(o, (25,25))
o = o.convert_alpha()
one = pygame.image.load("1.jpg")
one = pygame.transform.scale(one, (25,25))
one = one.convert_alpha()
two = pygame.image.load("2.jpg")
two = pygame.transform.scale(two, (25,25))
two = two.convert_alpha()
three = pygame.image.load("3.jpg")
three = pygame.transform.scale(three, (25,25))
three = three.convert_alpha()
four = pygame.image.load("4.png")
four = pygame.transform.scale(four, (25,25))
four = four.convert_alpha()
five = pygame.image.load("5.png")
five = pygame.transform.scale(five, (25,25))
five = five.convert_alpha()
six = pygame.image.load("6.jpg")
six = pygame.transform.scale(six, (25,25))
six = six.convert_alpha()
seven = pygame.image.load("7.jpg")
seven = pygame.transform.scale(seven, (25,25))
seven = seven.convert_alpha()

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = [ o,  one,  two,  three,  four,  five,  six,  seven,  o ]
figures   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

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
        surface.blit(COLOURS[self.clr], (x,y))
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)

    def move_up(self):
        self.row = self.row - 1

    def move_down(self):
        self.row = self.row +1
               

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo
        self._colOffsets = [0]*blocksNo  #@@
        self._rowOffsets = [0]*blocksNo  #@@

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] #@@
            blockROW = self.row+self._rowOffsets[i] #@@
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
###########################################################################################
# 9.  Add code here that appends the blocks of the other object to the self.blocks list.
#     Use a for loop to take each individual block from the other.blocks list
############################################################################################
        for block in other.blocks:
            self.blocks.append(block)


#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print (block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows, score, tetris):
        score=0
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
            if len(fullRows) == 4:
                score += 200
                tetris += 1
                a = pygame.mixer.Sound("point.wav")
                a.play(0)
            else:
                score += 100
                tetris = 0
                a = pygame.mixer.Sound("point.wav")
                a.play(0)
            if tetris > 1:
                score += 400
        return score
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1, _rot = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] #@@
        self._rowOffsets = [-1,-1, 0, 0] #@@
        self._rotate() #@@
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[1, 0, 0, 0], [-1,-1, 0, 1], [ -1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [1, 0, 0, 0], [-1,-1, 0, 1], [ -1, 0, 0, 0]] #
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] #@@
        self._rowOffsets = _rowOffsets[self._rot] #@@
        self._update() #@@

    def move_left(self):                
        self.col = self.col - 1                   
        self._update() #@@
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() #@@
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() #@@
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() #@@

    def rotateClkwise(self):
        self._rot = (self._rot +1) %4
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot -1) %4
        self._rotate()

#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i  #@@
        self._update() #@@
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i #@@
        self._update() #@@


class Shadow(Shape):
    """
        The outline of a tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation
    """

    def __init__(self, col=1, row=1, clr=1, _rot=1):
        Shape.__init__(self, col, row, clr, _rot)
        self.blocks = [Block()] * 4

    def draw(self, surface, GRIDSIZE=25):
        for i in range(len(self.blocks)):
            blockCOL = self.col + self._colOffsets[i]
            blockROW = self.row + self._rowOffsets[i]
            blockCLR = self.clr
            x = blockCOL * GRIDSIZE
            y = blockROW * GRIDSIZE
            pygame.draw.rect(surface, WHITE, (x, y, GRIDSIZE, GRIDSIZE), 2)

    def drop(self, other, third):
        while True:
            self.move_down()
            if self.collides(other) or self.collides(third):
                return True

    def rotateClk(self, floor, obstacles):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """

        if self.clr == 1:  # (default rotation)
            #   o             o o                o
            # o x               x o            x o          o x
            # o                                o              o o
            _colOffsets = [[-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, -1]]  #
            _rowOffsets = [[1, 0, 0, -1], [-1, -1, 0, 0], [-1, 0, 0, 1], [1, 1, 0, 0]]  #
        elif self.clr == 2:  #
            # o                 o o           o
            # o x             o x             x o             x o
            #   o                               o           o o
            _colOffsets = [[-1, -1, 0, 0], [1, 0, 0, -1], [1, 1, 0, 0], [-1, 0, 0, 1]]  #
            _rowOffsets = [[-1, 0, 0, 1], [-1, -1, 0, 0], [1, 0, 0, -1], [1, 1, 0, 0]]  #
        elif self.clr == 3:  #
            #   o             o                o o
            #   x             o x o            x           o x o
            # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0], [1, 1, 0, -1]]  #
            _rowOffsets = [[1, 1, 0, -1], [-1, 0, 0, 0], [-1, -1, 0, 1], [1, 0, 0, 0]]  #
        elif self.clr == 4:  #
            # o o                o             o
            #   x            o x o             x           o x o
            #   o                              o o         o
            _colOffsets = [[1, 0, 0, 0], [-1, -1, 0, 1], [-1, 0, 0, 0], [1, 1, 0, -1]]  #
            _rowOffsets = [[1, 1, 0, -1], [1, 0, 0, 0], [-1, -1, 0, 1], [-1, 0, 0, 0]]  #
        elif self.clr == 5:  # o                              o
            #   o                              x
            #   x            o x o o           o          o o x o
            #   o                              o
            _colOffsets = [[0, 0, 0, 0], [2, 1, 0, -1], [0, 0, 0, 0], [-2, -1, 0, 1]]  #
            _rowOffsets = [[-2, -1, 0, 1], [0, 0, 0, 0], [2, 1, 0, -1], [0, 0, 0, 0]]  #
        elif self.clr == 6:  #
            #   o              o                o
            # o x            o x o              x o         o x o
            #   o                               o             o
            _colOffsets = [[0, -1, 0, 0], [-1, 0, 0, 1], [0, 1, 0, 0], [1, 0, 0, -1]]  #
            _rowOffsets = [[1, 0, 0, -1], [0, -1, 0, 0], [-1, 0, 0, 1], [0, 1, 0, 0]]  #
        elif self.clr == 7:  #
            # o o            o o               o o          o o
            # o x            o x               o x          o x
            #
            _colOffsets = [[-1, -1, 0, 0], [-1, -1, 0, 0], [-1, -1, 0, 0], [-1, -1, 0, 0]]  # @@
            _rowOffsets = [[0, -1, 0, -1], [0, -1, 0, -1], [0, -1, 0, -1], [0, -1, 0, -1]]  # @@
        self._colOffsets = _colOffsets[self._rot]  # @@
        self._rowOffsets = _rowOffsets[self._rot]  # @@
        self._update()  # @@
        if self.drop(floor, obstacles):  # drops the shadow until it hits an object
            self.move_up()
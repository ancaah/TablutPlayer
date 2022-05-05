from ast import Constant
from operator import truediv
import socket
import struct
import json
from tracemalloc import start
from tools import Pawn
from aima.search import *
from aima.utils import *
from aima.reporting import *

##################################
# The Tablut Player, indeed.
##################################
 
class TablutPlayer(Problem):

    # This function, if used giving as parameters two cells in some Camps, returns true if they belong to the same Camp 
    def isSameCamp(_from, _to):
        if abs(_from[0] - _to[0]) + abs(_from[1] - _to[1]) <= 2: 
            return True
        else: return False

    def freeKingPaths(self, state):
        kingCol = self.king_position[1]
        kingRow = self.king_position[0]

        counter = 0

        # Check if up and down escapes are free
        # Case 1 - only up
        if kingCol in [1, 7] and kingRow < 4:    
            i = kingRow - 1 
            while i >= 0 and state[i,kingCol] == Pawn.EMPTY.value:
                i = i - 1
            if i < 0: counter = counter + 1 # Up escape path is free
        # Case 2 - up and down
        if kingCol in [2, 6]:    
            i = kingRow - 1 
            while i >= 0 and state[i,kingCol] == Pawn.EMPTY.value:
                i = i - 1
            if i < 0: counter = counter + 1 # Up escape path is free

            i = kingRow + 1 
            while i <= 8 and state[i,kingCol] == Pawn.EMPTY.value:
                i = i + 1
            if i < 0: counter = counter + 1 # Up escape path is free

        # Check if down escape is free
        if kingCol in [1, 7] and kingRow > 4:    
            i = kingRow + 1 
            while i <= 8 and state[i,kingCol] == Pawn.EMPTY.value:
                i = i + 1
            if i > 8: counter = counter + 1 # Down escape path is free

        # Check if left escape is free
        if kingCol in [1, 7] and kingRow < 4:    
            i = kingRow - 1 
            while i >= 0 and state[i,kingCol] == Pawn.EMPTY.value:
                i = i - 1
            if i == -1: counter = counter + 1 # Up escape path is free


        for i in range(0,9):
            if state[i, kingCol] != Pawn.EMPTY.value:

        

    def __init__(self, color, timeout, initial, king_position = [4,4] , goal = None):
        self.color = color
        self.king_position = king_position
        self.initial = initial
        self.timeout = timeout

        # Array of Camp cells (a4, a5, a6, b5, i4, ...)
        self.camps = [[3,0], [4,0], [5,0], [4,1], [3,8], [4,8], [5,8], [4,7], [0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]]
        
        #self.goal = goal
        # Goal is accomplished when the KiNG reaches one of the escape Cells. That's why in this case our goal variable
        # is a list of Escape Cells (similar to the Camp cells). This array is actually useful only for WHITE Player
        self.goal = [[0,1], [0,2], [0,6], [0,7], [8,1], [8,2], [8,6], [8,7], [1,0], [2,0], [6,0], [7,0], [1,8], [2,8], [6,8], [7,8]]

        Problem.__init__(self, self.initial, goal)


    def actions(self, state):
        """Just write all the actions executable in this state. First of all check if the state is valid, then initialize a vector e.g. result[] and with a list of condition on the state just fill it with all possible actions. e.g.: 
        m, c, b = state
        result = []
        if m > 0 and c > 0 and b:
            result.append('MC->')
        if ....
        return result

        Tablut: the actions given must be the couple of index (i,j) of the pawn you want to move and where
        """

        # List of possible moves for a given state
        result = []

        # Variables that tells if you *can* keep moving in a given direction, if false it means you found an obstacle
        up, down, right, left = (True, True, True, True)
        
        # WIP, MAYBE SHOULD IMPLEMENT IT to ease the process of checking up true, down true, left true, right true
        #keepGoing = True

        for i in range(0,9):
            for j in range (0,9):
                # If [i,j] is an empty cell, just do nothing
                if state[i,j] != Pawn.EMPTY.value:

                    # The selected cell has a White pawn in it
                    if state[i,j] == Pawn.WHITE.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 8: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1

                    up, down, right, left = (True, True, True, True)

                    # The selected cell has a Black pawn in it
                    if state[i,j] == Pawn.BLACK.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if self.isSameCamp((newRow, j), cell) == False and cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if self.isSameCamp((newRow, j), cell) == False and cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if self.isSameCamp(cell, (i, newCol)) == False and cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 9: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if self.isSameCamp(cell, (i, newCol)) == False and cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1
                          
                    up, down, right, left = (True, True, True, True)
                    
                    # The selected cell has a KiNG in it  
                    if state[i,j] == Pawn.KING.value:

                        # K variable moves the pawn in the matrix
                        k = 1
                        while k < 8 and (up == True or down == True or right == True or left == True):
                            
                            # Check if you can keep moving up
                            if up == True:
                                newRow = i-k
                                
                                # Check if index is out of bounds
                                if newRow == 0: up = False
                                
                                if up:
                                    # Check if the destination cell is a Camp
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            up = False
                                            break
                                    # Check if the destination cell is the Castle
                                    if newRow == 4 and j == 4:
                                        up = False

                                    # Check if you found another Pawn/King
                                    if up and state[newRow,j] != Pawn.EMPTY.value: up = False
                                    # If this is a proper move, add it to the result in a tuple: (from, to)
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving down
                            if down == True:
                                newRow = i+k
                                if newRow == 8: down = False
                                
                                if down:
                                    for cell in self.camps:
                                        if cell[0] == newRow and cell[1] == j:
                                            down = False
                                            break
                                    if newRow == 4 and j == 4:
                                        up = False
                                    
                                    if down and state[newRow,j] != Pawn.EMPTY.value: down = False
                                    else: result.append(([i,j],[newRow,j]))

                            # Check if you can keep moving left
                            if left == True:
                                newCol = j-k
                                if newCol == 0: left = False
                                
                                if left:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            left = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if left and state[i,newCol] != Pawn.EMPTY.value: left = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Check if you can keep moving right
                            if right == True:
                                newCol = j+k
                                if newCol == 8: right = False
                                
                                if right:
                                    for cell in self.camps:
                                        if cell[0] == i and cell[1] == newCol:
                                            right = False
                                            break
                                    if i == 4 and newCol == 4:
                                        up = False
                                    
                                    if right and state[i,newCol] != Pawn.EMPTY.value: right = False
                                    else: result.append(([i,j],[i,newCol]))

                            # Checked all four direction, so we extend the "radius" (k) and iterate
                            k = k + 1

                    up, down, right, left = (True, True, True, True)

        
    def result(self, state = None, action = None):
        """ given the state, just return the result executing the action given

        Tablut: the result will be given from the server.
        """

        startingPosition, endingPosition = action
        pawn = state[startingPosition]
        state[startingPosition] = Pawn.EMPTY.value
        state[endingPosition] = pawn

        # if the king is moved, update his position
        if startingPosition[0] == self.king_position[0] and startingPosition[1] == self.king_position[1]:
            self.king_position = endingPosition 
        
        return state

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def goal_test(self, state):
        """Return True if KiNG reached an Escape Cell (White player)
            Return True if KiNG is captured (Black player)"""

        # Just a consideration: what if we already knew the King's position? ^^

        '''
        # Search for the KiNG
        found = False
        i, j = (0, 0)
        while i < 9 and found == False:
            while j < 9 and found == False:
                if state[i,j] == Pawn.KING.value:
                    found = True 
                else: j = j + 1
            if found == False: i = i + 1
        '''

        i,j = self.king_position

        
        # Player WHITE
        if self.color == "WHITE":
            # Check if the KiNG reached an Escape cell
            for cell in self.goal:
                if cell[0] == i and cell[1] == j:
                    return True

        # Player BLACK
        elif self.color == "BLACK":
            # Check KiNG's sorroundings
            blocks = 0
            # KiNG in the Castle
            if i == 4 and j == 4:
                if state[i+1,j] == Pawn.BLACK.value: blocks = blocks + 1
                if state[i-1,j] == Pawn.BLACK.value: blocks = blocks + 1
                if state[i,j+1] == Pawn.BLACK.value: blocks = blocks + 1
                if state[i,j-1] == Pawn.BLACK.value: blocks = blocks + 1
                if blocks == 4: return True
            
            # KiNG next to the Castle
            elif abs(i - 4) + abs(j - 4) == 1:
                if state[i+1,j] == Pawn.BLACK.value or (i+1 == 4 and j == 4): blocks = blocks + 1
                if state[i-1,j] == Pawn.BLACK.value or (i-1 == 4 and j == 4): blocks = blocks + 1
                if state[i,j+1] == Pawn.BLACK.value or (i == 4 and j+1 == 4): blocks = blocks + 1
                if state[i,j-1] == Pawn.BLACK.value or (i == 4 and j-1 == 4): blocks = blocks + 1
                if blocks == 4: return True
            
            # KiNG is in another place of the map
            else:
                if state[i+1,j] == Pawn.BLACK.value or [i+1,j] in self.camps: blocks = blocks + 1
                if state[i+1,j] == Pawn.BLACK.value or [i+1,j] in self.camps: blocks = blocks + 1
                if state[i+1,j] == Pawn.BLACK.value or [i+1,j] in self.camps: blocks = blocks + 1
                if state[i+1,j] == Pawn.BLACK.value or [i+1,j] in self.camps: blocks = blocks + 1
                if blocks >= 2: return True
                
        return False
        
    """ Informated strategies needs to implement the h function.
    The notion of heuristic: a function that estimates (with a certain error) the distance of astate from the goal… admissible? consistent? """
    def h(self, node):
        """e.g: 
        m, c,  b = node.state
        return m + c - b """




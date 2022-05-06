from ast import Constant
import socket
import struct
import json
from tools import Pawn
from tools import Utils
from aima.search import *
from aima.utils import *
from aima.reporting import *
from aima.games import *

##################################
# The Tablut Player, indeed.
##################################
 
class TablutPlayer(Game):

    # dir is the direction to check: "up", "down", "left" or "right"
    # Return True if the given direction doesn't have any obstacles between the KiNG and the Escape Cells
    # Obstacles are Camps, other Pawns, and the Castle
    def checkIfKingPathIsFree(self, state, _d):
        # Just one between row and col will change, depending on the direction that needs to get checked
        curr_pos = self.king_position.copy()
        Utils.check_next_cell(Utils, curr_pos, _d)
        
        while self.cellIsFree(state, curr_pos):
            Utils.check_next_cell(Utils, curr_pos, _d)

        if Utils.cellIsOutOfMatrix(Utils, curr_pos):
            return True # Escape path in direction dir is free
        return False

    def freeKingPaths(self, state):
        
        counter = 0
        # Count how many Escapes are free
        counter += self.checkIfKingPathIsFree(state, "up")
        counter += self.checkIfKingPathIsFree(state, "right")
        counter += self.checkIfKingPathIsFree(state, "down")
        counter += self.checkIfKingPathIsFree(state, "left")

        return counter

    def __init__(self, color, timeout, initial, king_position = [4,4] , goal = None):
        self.color = color
        self.turn = color
        self.king_position = king_position
        self.initial = initial
        self.timeout = timeout

        # Array of Camp cells (a4, a5, a6, b5, i4, ...)
        self.camps = [[3,0], [4,0], [5,0], [4,1], [3,8], [4,8], [5,8], [4,7], [0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]]
        self.castle = [4,4]
        #self.goal = goal
        # Goal is accomplished when the KiNG reaches one of the escape Cells. That's why in this case our goal variable
        # is a list of Escape Cells (similar to the Camp cells). This array is actually useful only for WHITE Player
        self.goal = [[0,1], [0,2], [0,6], [0,7], [8,1], [8,2], [8,6], [8,7], [1,0], [2,0], [6,0], [7,0], [1,8], [2,8], [6,8], [7,8]]
    # Returns true if it's a possible destination cell
    # It is not possible to cross or end the movement on cells with Checkers, on the Castle, or on Camp cells
    # Exception! The black checkers can move in the cells of their starting Camp until they leave it. After that, they can’t go back in.
    def cellIsFree(self, state, position, isBlack = False, starting_pos = None):
        # Follows a list of controls on the destination
        # Check if index is out of bounds or not empty
        if Utils.cellIsOutOfMatrix(position): return False
        # Check if you found another Pawn/King
        elif state[position] != Pawn.EMPTY.value: return False
        # Check if the destionation cell is a Camp.
        elif not isBlack and position in self.camps: return False
        # If it's Black, check also if isSameCamp
        elif isBlack and starting_pos is not None:
            if not Utils.isSameCamp(position,starting_pos): return False

        return True


    # Return a list of the possible moves in the given direction for a Black Pawn
    def giveReachableCells_Black(self, result, state, position, _d):
        # Starting position
        starting_pos = position.copy()
        curr_pos = position.copy()
        dummy_state = np.copy(state)

        # Just one between row and col will change, depending on the direction that needs to get checked
        Utils.check_next_cell(Utils, curr_pos, _d)

        while self.cellIsFree(state,curr_pos, True, starting_pos):
            # We do this to check the freeKingPaths later
            Utils.changeCell(dummy_state, old_position, Pawn.EMPTY.value)
            Utils.changeCell(dummy_state, curr_pos, Pawn.BLACK.value)

            old_position = curr_pos.copy()

            Utils.check_next_cell(Utils, curr_pos, _d)

            # This is important, if the move we just found gives the White team a winning condition we don't add it
            if self.freeKingPaths(dummy_state) == 0:
                result.append(((starting_pos),(curr_pos)))
        
        return result

    # Return a list of the possible moves in the given direction for a White Pawn
    def giveReachableCells_White(self, result, state, position, _d, dummy_state = None, colorCondition = None):
        # Starting position
        starting_pos = position.copy()
        curr_pos = position.copy()
        # Just one between row and col will change, depending on the direction that needs to get checked
        Utils.check_next_cell(curr_pos, _d)
            
        while self.cellIsFree(state, curr_pos):
            position = Utils.check_next_cell(curr_pos, _d)
            result.append(((starting_pos),(curr_pos)))
        
        return result
    
    # This function returns the list of actions that the Black Player should expand
    def blackBehaviour(self, state):
        result = []
        for i in range(0,9):
            for j in range (0,9):
                # The selected cell has a Black pawn in it, that means we could move it
                if state[i,j] == Pawn.BLACK.value:
                    # Check actions in up, right, down and left direction
                    position = [i,j]
                    self.giveReachableCells_Black(result, state, position, "up")
                    self.giveReachableCells_Black(result, state, position, "right")
                    self.giveReachableCells_Black(result, state, position, "down")
                    self.giveReachableCells_Black(result, state, position, "left")
        return result

    # This function returns the list of actions that the White Player should expand
    def whiteBehaviour(self, state):
        result = []

        for i in range(0,9):
            for j in range (0,9):
                # The selected cell has a White pawn in it, that means we could move it
                if state[i,j] == Pawn.WHITE.value or state[i,j] == Pawn.KING.value:
                    # Check actions in up, right, down and left direction
                    position = [i,j]
                    self.giveReachableCells_White(result, state, position,"up")
                    self.giveReachableCells_White(result, state, position, "right")
                    self.giveReachableCells_White(result, state, position, "down")
                    self.giveReachableCells_White(result, state, position, "left")

        return result

    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    # Next the 4 methods we need to implement to use Game class from aima library: actions, result, utility and terminal_test
    # I think that this method now should just call blackBehaviour (implemented) or whiteBehaviour (TODO)
    # depending on the player turn.
    # So there are a lot of pending changes to this method
    def actions(self, state):
        """Return a list of the allowable moves at this point."""

        # List of possible moves for a given state
        result = []

        if self.turn == "WHITE":
            result = self.whiteBehaviour(state)
            self.turn == "BLACK"
        else: 
            result = self.blackBehaviour(state)
            self.turn == "WHITE"

        return result
        

        
    def result(self, state = None, action = None):
        """Return the state that results from making a move from a state."""

        startingPosition, endingPosition = action
        pawn = state[startingPosition]
        state[startingPosition] = Pawn.EMPTY.value
        state[endingPosition] = pawn

        # if the king is moved, update his position
        if startingPosition[0] == self.king_position[0] and startingPosition[1] == self.king_position[1]:
            self.king_position = endingPosition 
        
        return state

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError


    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    ## All this will be moved to terminal_test (from Game)
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

        # NEED TO ADD WHICH TURN IS RIGHT NOW, SO THAT YOU DECIDE WHAT THE GOAL IS
        # also this method is shit so let's change that

        # Player WHITE
        if self.color == "WHITE":
            # Check if the KiNG reached an Escape cell
            if [i, j] in self.goal:
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




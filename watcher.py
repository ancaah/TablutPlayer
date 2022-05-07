import numpy as np
from tools import Utils, Pawn

##################################
# The board Watcher. 
# Will tell to player what's possible and what's not.
##################################
 
class Watcher():
    def __init__(self, king_position = [4,4] ):
        self.king_position = king_position
        # Array of Camp cells (a4, a5, a6, b5, i4, ...)
        self.camps = [[3,0], [4,0], [5,0], [4,1], [3,8], [4,8], [5,8], [4,7], [0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]]
        self.castle = [4,4]
        # Goal is accomplished when the KiNG reaches one of the escape Cells. That's why in this case our goal variable
        # is a list of Escape Cells (similar to the Camp cells). This array is actually useful only for WHITE Player
        self.goal = [[0,1], [0,2], [0,6], [0,7], [8,1], [8,2], [8,6], [8,7], [1,0], [2,0], [6,0], [7,0], [1,8], [2,8], [6,8], [7,8]]

    
    # dir is the direction to check: "up", "down", "left" or "right"
    # Return True if the given direction doesn't have any obstacles between the KiNG and the Escape Cells
    # Obstacles are Camps, other Pawns, and the Castle
    def checkIfKingPathIsFree(self, board, _d):
        # Just one between row and col will change, depending on the direction that needs to get checked
        curr_pos = self.king_position.copy()
        Utils.check_next_cell(curr_pos, _d)
        
        while self.cellIsFree(board, curr_pos):
            Utils.check_next_cell(curr_pos, _d)

        if Utils.cellIsOutOfMatrix(curr_pos):
            return True # Escape path in direction dir is free
        return False

    def freeKingPaths(self, board):
        
        counter = 0
        # Count how many Escapes are free
        counter += self.checkIfKingPathIsFree(board, "up")
        counter += self.checkIfKingPathIsFree(board, "right")
        counter += self.checkIfKingPathIsFree(board, "down")
        counter += self.checkIfKingPathIsFree(board, "left")

        return counter

    

    # Returns true if it's a possible destination cell
    # It is not possible to cross or end the movement on cells with Checkers, on the Castle, or on Camp cells
    # Exception! The black checkers can move in the cells of their starting Camp until they leave it. After that, they can’t go back in.
    def cellIsFree(self, board, position, isBlack = False, starting_pos = None):
        # Follows a list of controls on the destination
        # Check if index is out of bounds or not empty
        if Utils.cellIsOutOfMatrix(position): return False
        # Check if you found another Pawn/King
        elif board[position[0], position[1]] != Pawn.EMPTY.value: return False
        #Check if it's the castle
        elif position == [4,4]: return False
        # Check if the destionation cell is a Camp.
        elif not isBlack and position in self.camps: return False
        # If it's Black, check also if isSameCamp
        elif isBlack and starting_pos is not None:
            if not Utils.isSameCamp(position,starting_pos): return False

        # Always in bound.
        #print ("\nFree cell: ", position)
        return True


    # Return a list of the possible moves in the given direction for a Black Pawn
    def giveReachableCells_Black(self, result, board, position, _d):
        # Starting position
        starting_pos = position.copy()
        curr_pos = position.copy()
        dummy_board = np.copy(board)

        # Just one between row and col will change, depending on the direction that needs to get checked   
        # Moving first cell to check
        old_position = curr_pos.copy()
        curr_pos = Utils.check_next_cell(curr_pos, _d)

        while self.cellIsFree(board,curr_pos, True, starting_pos):
            # We do this to check the freeKingPaths later
            Utils.changeCell(dummy_board, old_position, Pawn.EMPTY.value)
            Utils.changeCell(dummy_board, curr_pos, Pawn.BLACK.value)
            # This is important, if the move we just found gives the White team a winning condition we don't add it
            # If the cell is valid add to the results
            if self.freeKingPaths(dummy_board) == 0:
                free_cell = curr_pos.copy()
                result.append(((starting_pos),(free_cell)))
            old_position = curr_pos.copy()
            # Move to the next cell to check
            curr_pos = Utils.check_next_cell(curr_pos, _d)

        return result

    # Return a list of the possible moves in the given direction for a White Pawn
    def giveReachableCells_White(self, result, board, position, _d, dummy_board = None, colorCondition = None):
        # Starting position
        starting_pos = position.copy()
        curr_pos = position.copy()
        
        # Just one between row and col will change, depending on the direction that needs to get checked
        # Move to the next cell 
        curr_pos = Utils.check_next_cell(curr_pos, _d)    
        # Check the cell, if it's free, add it to the possible reacheable cells.
        while self.cellIsFree(board, curr_pos):
            free_cell = curr_pos.copy() 
            result.append(((starting_pos),(free_cell)))
            # Moving to the next cell
            curr_pos = Utils.check_next_cell(curr_pos, _d)

        return result
    
    # This function returns the list of actions that the Black Player should expand
    def blackBehaviour(self, board):
        result = []
        for i in range(0,9):
            for j in range (0,9):
                # The selected cell has a Black pawn in it, that means we could move it
                if board[i,j] == Pawn.BLACK.value:
                    # Check actions in up, right, down and left direction
                    position = [i,j]
                    self.giveReachableCells_Black(result, board, position, "up")
                    self.giveReachableCells_Black(result, board, position, "right")
                    self.giveReachableCells_Black(result, board, position, "down")
                    self.giveReachableCells_Black(result, board, position, "left")
        return result

    # This function returns the list of actions that the White Player should expand
    def whiteBehaviour(self, board):
        result = []

        for i in range(0,9):
            for j in range (0,9):
                # The selected cell has a White pawn in it, that means we could move it
                if board[i,j] == Pawn.WHITE.value or board[i,j] == Pawn.KING.value:
                    # Check actions in up, right, down and left direction
                    position = [i,j]
                    self.giveReachableCells_White(result, board, position,"up")
                    self.giveReachableCells_White(result, board, position, "right")
                    self.giveReachableCells_White(result, board, position, "down")
                    self.giveReachableCells_White(result, board, position, "left")
        
        return result


    def checkIfEat_BLACK(self, board, position, _d):
        curr_pos = position.copy()
        curr_pos = Utils.check_next_cell(curr_pos, _d)
        eat_pos = curr_pos.copy()
        if Utils.cellIsIntoMatrix(curr_pos):
            if board[eat_pos[0], eat_pos[1]] == Pawn.WHITE.value:
                curr_pos = Utils.check_next_cell(curr_pos, _d)
                if Utils.cellIsIntoMatrix(curr_pos): 
                    if curr_pos == Pawn.BLACK.value or curr_pos in self.camp:
                        # Eat!
                        board[eat_pos[0], eat_pos[1]] = Pawn.EMPTY.value


    def checkIfEat_WHITE(self, board, position, _d):
        curr_pos = position.copy()
        curr_pos = Utils.check_next_cell(curr_pos, _d)
        eat_pos = position.copy()
        if Utils.cellIsIntoMatrix(curr_pos):
            if board[eat_pos[0], eat_pos[1]] == Pawn.BLACK.value:
                curr_pos = Utils.check_next_cell(curr_pos, _d)
                if Utils.cellIsIntoMatrix(curr_pos):
                    if  curr_pos == Pawn.WHITE.value:
                        # Eat!
                        board[eat_pos[0], eat_pos[1]] = Pawn.EMPTY.value

    def doMove(self,board,action, player):
        startingPosition, endingPosition = action
        pawn = board[startingPosition]
        board[startingPosition] = Pawn.EMPTY.value
        board[endingPosition] = pawn
        
        # if the king is moved, update his position
        if startingPosition[0] == self.king_position[0] and startingPosition[1] == self.king_position[1]:
            self.king_position = endingPosition 
     
        # Check if someone has been eated!
        # ATTENTION! The board is going to be modified is something is eated.

        if player == "WHITE":
            self.checkIfEat_WHITE(board, endingPosition, "up")
            self.checkIfEat_WHITE(board, endingPosition, "down")
            self.checkIfEat_WHITE(board, endingPosition, "left")
            self.checkIfEat_WHITE(board, endingPosition, "right")
        
        else: 
            self.checkIfEat_BLACK(board, endingPosition, "up")
            self.checkIfEat_BLACK(board, endingPosition, "down")
            self.checkIfEat_BLACK(board, endingPosition, "left")
            self.checkIfEat_BLACK(board, endingPosition, "right")

    
    # This methods return 1 if WHITE wins, -1 if BLACK wins, otherwise 0
    # Maybe it's possible to identify other values, e.g. 0.3 when eating a pawn
    def compute_utility(self,board):
    #   Check if BLACK won
        blocks = 0
        
        i = self.king_position[0]
        j = self.king_position[1]

        # WHITE win possible board
        # KiNG is Free
        if self.king_position in self.goal:
            return 1

        # BLACK win possible boards
        # KiNG in the Castle (4 blocks needed)
        if i == 4 and j == 4:
            if board[i+1,j] == Pawn.BLACK.value: blocks = blocks + 1
            if board[i-1,j] == Pawn.BLACK.value: blocks = blocks + 1
            if board[i,j+1] == Pawn.BLACK.value: blocks = blocks + 1
            if board[i,j-1] == Pawn.BLACK.value: blocks = blocks + 1
            if blocks == 4: return -1
        
        # KiNG next to the Castle (3 blocks needed)
        elif abs(i - 4) + abs(j - 4) == 1:
            if board[i+1,j] == Pawn.BLACK.value or (i+1 == 4 and j == 4): blocks = blocks + 1
            if board[i-1,j] == Pawn.BLACK.value or (i-1 == 4 and j == 4): blocks = blocks + 1
            if board[i,j+1] == Pawn.BLACK.value or (i == 4 and j+1 == 4): blocks = blocks + 1
            if board[i,j-1] == Pawn.BLACK.value or (i == 4 and j-1 == 4): blocks = blocks + 1
            if blocks == 4: return -1
        
        # KiNG is in another place of the map (2 blocks needed)
        else:
            if (board[i+1,j] == Pawn.BLACK.value or [i+1,j] in self.camps) and (board[i-1,j] == Pawn.BLACK.value or [i-1,j] in self.camps): 
                return -1
            elif (board[i,j+1] == Pawn.BLACK.value or [i,j+1] in self.camps) and (board[i,j-1] == Pawn.BLACK.value or [i,j-1] in self.camps): 
                return -1

        return 0
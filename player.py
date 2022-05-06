from ast import Constant
import socket
import struct
import json
from tools import Pawn, Utils
from watcher import Watcher
from aima.search import *
from aima.utils import *
from aima.reporting import *
from aima.games import *

##################################
# The Tablut Player, indeed.
##################################
 
class TablutPlayer(Game):

    def __init__(self, color, timeout, initial_board, king_position = [4,4]):
     
        # GameState = namedtuple('GameState', 'to_move, utility, board, moves')
        # self.initial will be the GameState
        self.watcher = Watcher(king_position)
        board = initial_board
        self.initial = GameState(to_move=color, 
                                utility=self.watcher.compute_utility(board), 
                                board=board, 
                                moves=self.getAllMoves(board, color))
        self.timeout = timeout

    def getAllMoves(self, board, player):
        if player == "WHITE":
            return self.watcher.whiteBehaviour(board)
        else: return self.watcher.blackBehaviour(board)
         
    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    # Next the 4 methods we need to implement to use Game class from aima library: 
    # actions, result, utility and terminal_test

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        # List of possible moves for a given state
        player = state.to_move
        board = copy.deepcopy(state.board)
        #print(state.moves)
        if player == "WHITE":
            return self.watcher.whiteBehaviour(board)
        else: return self.watcher.blackBehaviour(board)         

        
    def result(self, state, action):
        """Return the state that results from making a move from a state."""
        board = copy.deepcopy(state.board)
        player = state.to_move

        # Make the given move on the copied board, change turn 
        self.watcher.doMove(board,action)
        player = ("BLACK" if player == "WHITE" else "WHITE")
        
        return GameState(to_move=player,
                        utility= self.watcher.compute_utility(board),
                        board = board,
                        moves = self.getAllMoves(board, player))

    def utility(self, state, player):
        """Return the value of this final state to player.
        1 for win, -1 for loss, 0 otherwise. 
        """
        # Will return the value given by state.utility -> watcher.compute_utility result
        # Maybe there is possible to calibrate more accurate values
        return state.utility if player == "WHITE" else -state.utility


    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        # It's a terminal state if it's equal to 1 or -1 
        return state.utility != 0
        



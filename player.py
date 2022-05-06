from ast import Constant
import socket
import struct
import json
from tools import Pawn, Utils
from board import BoardManager
from aima.search import *
from aima.utils import *
from aima.reporting import *
from aima.games import *

##################################
# The Tablut Player, indeed.
##################################
 
class TablutPlayer(Game):

    def __init__(self, color, timeout, initial_board, king_position = [4,4]):
        self.color = color
        self.turn = color
        self.king_position = king_position
        
        # GameState = namedtuple('GameState', 'to_move, utility, board, moves')
        # initial will be the state
        self.board_man = BoardManager()
        board = initial_board
        self.initial = GameState(to_move='WHITE', utility=0, board=board, moves=self.board_man.whiteBehaviour(board))
        self.timeout = timeout





    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    # Next the 4 methods we need to implement to use Game class from aima library: actions, result, utility and terminal_test

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

        self.board.doMove(state,action)
        
        return state

    def utility(self, state, player):
        """Return the value of this final state to player.
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]
            
        """
        if self.turn == 'WHITE':
            return self.utils[state]
        else:
            return -self.utils[state]


    def terminal_test(self, state):
        """Return True if this is a final state for the game."""

        return self.board.isTerminalState(state)
        



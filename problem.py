import numpy as np
from search import *
from collections import defaultdict, deque, Counter
from reporting import *
from enum import Enum


class Pawn(Enum):
    WHITE = 1
    BLACK = 2
    KING = 3


class TabSolve(Problem):

    def __init__(self, initial, goal):
        """Constructor"""

    def path_cost(self, c, state1, action, state2):

    def actions(self, state):

    def result(self, state, action):

    def goal_test(self, state):

    def h(self, node):


# Utils

def printMatrix(state):
    X = np.empty((9, 9), dtype=int)

    for i in range(0,9):
        for j in range(0,9):
            if S[i][j] is None:
                X[i][j] = 0
            else:
                X[i][j] = S[i][j].value

    print(X)

# main

S = np.empty((9, 9), dtype=Pawn)

# Initial State
# horizontal black pawns
S[0][3:6] = Pawn.BLACK
S[1][4] = Pawn.BLACK
S[8][3:6] = Pawn.BLACK
S[7][4] = Pawn.BLACK

# vertical black pawns
for i in range(3,6):
    S[i][0] = Pawn.BLACK
    S[i][8] = Pawn.BLACK

S[4][1] = Pawn.BLACK
S[4][7] = Pawn.BLACK

# white pawns
S[4][4] = Pawn.KING
for i in range(2,4):
    S[i][4] = Pawn.WHITE
    S[i][4] = Pawn.WHITE
for i in range(5,7):   
    S[i][4] = Pawn.WHITE
    S[i][4] = Pawn.WHITE

printMatrix(S)


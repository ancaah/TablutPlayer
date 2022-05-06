from http import server
import sys
from aima.games import random_player
from player import TablutPlayer
from tools import Talker
from aima.games import *

#Configuration
name = "ASimplexMind"
color = sys.argv[1]
timeout = int(sys.argv[2])
# if arg is null localhost is chosen
if len(sys.argv) == 4: 
    server_address = sys.argv[3]
else: server_address = 'localhost'

print("\nConnection to: " + server_address)

talker = Talker(name, color, server_address)
board, _ , _ = talker.enstablish_connection()
tp = TablutPlayer(color, timeout, board)
print("\nInitial state:")
#tp.display(state)
print(board)

goal = False

#while(goal is False):
    #solve the problem. 
    #tp.solve() returns from i,j to i,j
state = GameState(to_move=color, 
                utility=tp.watcher.compute_utility(board), 
                board=board, 
                moves=tp.getAllMoves(board, color))
move = random_player(tp, state)
print(move)
#send the move
#move = talker.send_move([4,3], [2,3])
move = talker.send_move(move)
#get the new state
board, turn ,king_position = talker.get_state()
print("\nMy move:  " + move)
#print(board)
print("\nWaiting for enemy move....")
board, turn ,king_position = talker.get_state()
print("\nEnemy move:")
#tp.display(state)
print(board)
#create the new problem
#tp = TablutPlayer(color, timeout, board, king_position) 
exit








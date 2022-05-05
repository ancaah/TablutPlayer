from http import server
import sys
from player import TablutPlayer
from tools import Talker

#Configuration
name = "ASimplexMind"
color = sys.argv[1]
timeout = int(sys.argv[2])
# if arg is null localhost is chosen
if len(sys.argv) == 4: 
    server_address = sys.argv[3]
else: server_address = 'localhost'

print(server_address)

talker = Talker(name, color, server_address)
state, _ , _ = talker.enstablish_connection()
tp = TablutPlayer(color, timeout, state)
print("\nInitial state:")
print(state)

goal = False

while(goal is False):
    #solve the problem. 
    #tp.solve() returns from i,j to i,j

    #send the move
    move = talker.send_move([4,3], [2,3])
    #get the new state
    state, turn ,king_position = talker.get_state()
    print("\nMy move:  " + move)
    print(state)
    print("\nWaiting for enemy move....")
    state, turn ,king_position = talker.get_state()
    print("\nEnemy move:")
    print(state)
    #create the new problem
    tp = TablutPlayer(color, timeout, state, king_position) 









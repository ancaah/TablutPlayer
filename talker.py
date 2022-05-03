from ast import Constant
import socket
import struct
import json
import numpy as np
from enum import Enum

#############################
# Talker will manage the connection and all the communication to and from the server  
# Additionally, it will converter the json state into matrix using Converter class.
#############################

class Talker: 
    # Configuration 
    def __init__(self, color, player_name, converter = None, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        else:
            self.sock = sock

        if converter is None:
            self.converter = Converter()
        else:
            self.converter = converter
        
        self.color = color
        self.player_name = player_name
        self.enstablish_connection()

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def enstablish_connection(self):
    
        if self.color == 'WHITE':
            # Connect the socket to the port where the server is listening
            server_address = ('localhost', 5800)
        elif self.color == 'BLACK':
            #  Connect the socket to the port where the server is listening
            server_address = ('localhost', 5801)
        else:
            raise Exception("Se giochi o sei bianco oppure sei nero")
        
        # Enstablish connection
        self.sock.connect(server_address)

        # Using struct lib in order to represent data as python bytes objects
        # struct.pack(format, val1, val2...) 
        # '>i' means Big Endian(used in network), integer returns a bytes object. 
        self.sock.send(struct.pack('>i', len(self.player_name)))
        self.sock.send(self.player_name.encode())


    # Returning the state as a matrix and who's turn
    def get_state(self):

        len_bytes = struct.unpack('>i', self.recvall(4))[0]
        current_state_server_bytes = self.sock.recv(len_bytes)
        # Converting byte into json 
        json_state = json.loads(current_state_server_bytes)
        state, turn = self.converter.json_to_matrix(json_state)
        return state, turn 
    
    # sends move, using Converter to convert move 
    # out: e.g. {"from": "d3", "to": "f5", "turn": "WHITE"}
    def send_move(self, _from, _to):
        turn = self.color
        from_s = self.converter.box_to_string(_from[0], _from[1])
        to_s =  self.converter.box_to_string(_to[0], _to[1])

        move = json.dumps({
            "from": from_s, 
            "to" : to_s,
            "turn" : turn
        })

        print(move)
        self.sock.send(struct.pack('>i', len(move)))
        self.sock.send(move.encode())



class Pawn(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    KING = 3

class Converter:

    def json_to_matrix(self, json_state):
    
        # Convert to list
        data = list(json_state.items())
        # Convert to array
        ar = np.array(data, dtype = object)
        # Selecting board (the array is (2,2) matrix, it has board and turn info)
        board_array = np.array(ar[0,1], dtype=object)   
        turn = ar[1,1]
        # Converting in a numerical matrix
        state = np.zeros((9,9), dtype = Pawn)
        for i in range(0,9):
            for j in range (0,9):
                if board_array[i,j] == 'EMPTY':
                    state[i,j] = Pawn.EMPTY.value
                elif board_array[i,j] == 'WHITE':
                    state[i,j] = Pawn.WHITE.value
                elif board_array[i,j] == 'BLACK':
                    state[i,j] = Pawn.BLACK.value
                elif board_array[i,j] == 'KING':
                    state[i,j] = Pawn.KING.value

        print(state)
        
        return state, turn

    def box_to_string(self, row, col):
        # converting row/call index into alphanumerical value e.g. h1 (97 is the value of a in ASCII table)
        res = "" + chr(97 + col) + str(1 + row)
        return res                    
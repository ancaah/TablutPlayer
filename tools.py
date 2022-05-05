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
    def __init__(self, name, color, server_ip = 'localhost', converter = None, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        else:
            self.sock = sock

        if converter is None:
            self.converter = Converter()
        else:
            self.converter = converter
        
        self.color = color
        self.name = name
        self.server_ip = server_ip

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # connetion and first state receive
    def enstablish_connection(self):
    
        if self.color == 'WHITE':
            # Connect the socket to the port where the server is listening
            server_address = (self.server_ip, 5800)
        elif self.color == 'BLACK':
            #  Connect the socket to the port where the server is listening
            server_address = (self.server_ip, 5801)
        else:
            raise Exception("Se giochi o sei bianco oppure sei nero")
        
        # Enstablish connection
        self.sock.connect(server_address)

        # Using struct lib in order to represent data as python bytes objects
        # struct.pack(format, val1, val2...) 
        # '>i' means Big Endian(used in network), integer returns a bytes object. 
        self.sock.send(struct.pack('>i', len(self.name)))
        self.sock.send(self.name.encode())

        return self.get_state()


    # Returning the state as a matrix, who's turn and king_pos
    def get_state(self):

        len_bytes = struct.unpack('>i', self.recvall(4))[0]
        current_state_server_bytes = self.sock.recv(len_bytes)
        # Converting byte into json 
        json_state = json.loads(current_state_server_bytes)
        state, turn, king_position = self.converter.json_to_matrix(json_state)
        return state, turn, king_position
    
    # sends move, using Converter to convert move 
    # it returns the print of the move
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

        self.sock.send(struct.pack('>i', len(move)))
        self.sock.send(move.encode())
        return move


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
                    king_position = (i,j)

        return state, turn, king_position

    def box_to_string(self, row, col):
        # converting row/call index into alphanumerical value e.g. h1 (97 is the value of a in ASCII table)
        res = "" + chr(97 + col) + str(1 + row)
        return res                    

class Utils:
    # This function, if used giving as parameters **two cells in some Camps**, returns true if they belong to the same Camp 
    # This function CANNOT BEHAVE WELL if you change the dimensions of the checkerboard or the camps
    def isSameCamp(_from, _to):
        if abs(_from[0] - _to[0]) + abs(_from[1] - _to[1]) <= 2: 
            return True
        else: return False

    def inc(v):
        return v + 1

    def dec(v):
        return v - 1

    # Return True the given Cell is for sure out of the matrix, False otherwise
    def cellIsOutOfMatrix(row, col):
        if row < 0 or row > 8 or col < 0 or col > 8: return True
        return False

    # Return True if the given Cell is for sure into the matrix, False otherwise
    def cellIsIntoMatrix(row, col):
        if row >= 0 and row <= 8 and col >= 0 and col <= 8: return True
        return False   

from ast import Constant
import socket
import struct
import json

#############################
# Talker will manage the connection and all the communication to and from the server  
# Additionally, it will converter the json state into matrix
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
    
        if self.color == 'white':
            # Connect the socket to the port where the server is listening
            server_address = ('localhost', 5800)
        elif self.color == 'black':
            #  Connect the socket to the port where the server is listening
            server_address = ('localhost', 5801)
        else:
            raise Exception("Se giochi o sei bianco oppure sei nero")
        
        # Enstablish connection
        self.sock.connect(server_address)

        # Using struct lib in order to represent data as python bytes objects
        # struct.pack(format, val1, val2...) 
        # '>i' means Big Endian(used in network), integer
        # returns a bytes object. 
        self.sock.send(struct.pack('>i', len(self.player_name)))
        self.sock.send(self.player_name.encode())


    def get_state(self):

        len_bytes = struct.unpack('>i', self.recvall(4))[0]
        current_state_server_bytes = self.sock.recv(len_bytes)
            
        # Converting byte into json 
        json_state = json.loads(current_state_server_bytes)

        #print(current_state_server_bytes)
        #print(json_state)

        return json_state

        #return self.converter.json_to_matrix(json_state)

class Converter:
    def json_to_matrix(self, json_state):
        json_list = json.load(json_state)
        print(json_list)

    #def matrix_to_json(self, matrix):
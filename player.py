from ast import Constant
import socket
import struct
import json
from talker import Talker
from search import *
from utils import *
from reporting import *

##################################
# The Tablut Player, indeed. It will interface with Talker to speak to the server
##################################
 
class TablutPlayer:

    def __init__(self, color, player_name, goal = None, talker = None):
        if talker is None:
            self.talker = Talker(color, player_name)
        else:
             self.talker = talker
        
        self.initial = self.talker.get_state()
        print (self.initial)
        self.goal = goal
        Problem.__init__(self, self.initial, goal)


    def actions(self, state):
        """Just write all the actions executable in this state. First of all check if the state is valid, then initialize a vector e.g. result[] and with a list of condition on the state just fill it with all possible actions. e.g.: 
        m, c, b = state
        result = []
        if m > 0 and c > 0 and b:
            result.append('MC->')
        if ....
        return result
        """

        
    def result(self, state = None, action = None):
        """ given the state, just return the result executing the action given

        Tablut: the result will be given from the server. Talker will handle it!
        """
        
        return self.talker.get_state()

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    """ Informated strategies needs to implement the h function.
    The notion of heuristic: a function that estimates (with a certain error) the distance of astate from the goal… admissible? consistent? """
    def h(self, node):
        """e.g: 
        m, c,  b = node.state
        return m + c - b """





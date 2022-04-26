import numpy as np
from search import *
from utils import *
from reporting import *
from enum import Enum

class Cell(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 3
    KING = 4 
    WIN = 5


class myTablutPlayer(Problem):

    def __init__(self, initial, goal):
        """Constructor"""
        self.initial = initial
        self.goal = goal
        Problem.__init__(self, initial, goal)


    def actions(self, state):
        """Just write all the actions executable in this state. First of all check if the state is valid, then initialize a vector e.g. result[] and with a list of condition on the state just fill it with all possible actions. e.g.: 
        m, c, b = state
        result = []
        if m > 0 and c > 0 and b:
            result.append('MC->')
        if ....
        return result
        """

        
    def result(self, state, action):
        """ given the state, just return the result executing the action given
        e.g.:
        m, c, b = state
        if action == 'MC->':
            return (m - 1, c - 1, 0)
        elif action == 'MM->':
            return (m-2, c, 0)
        ....
        else:
            print("Is not possible to apply this action to this state.")
            return None
        """
        

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
 

 




tp = myTablutPlayer(np.zeros((9,9), dtype=np.int8))

for i in range(9):
    for j in range (9):
        


soln = breadth_first_tree_search(tp)
# print("Done!!!")
path = path_actions(soln)
print(path)
path = path_states(soln)
print(path)

report([
    breadth_first_tree_search,
    breadth_first_graph_search,
    # depth_first_tree_search,
    depth_first_graph_search,
    astar_search
    ],
    [tp])

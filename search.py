# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


class Node():
    """
    a node in a graph
    """
    def __init__(self, position, move = [], price = 0, father = None):

        self.position = position
        self.move = move
        self.price = price
        self.father = father

def search (problem , data_struct ):

  start_node = Node(problem.getStartState())
  nodes = {start_node.position: start_node}
  data_struct.push(start_node)
  found_goal = None
  
  while not data_struct.isEmpty():
      curr_node = data_struct.pop()
      if problem.isGoalState(curr_node.position):
        return curr_node.move
        #found_goal = curr_node
         
      for state, move, price in [ succ for succ in problem.getSuccessors(curr_node.position)] :
        #new_node = Node(state, curr_node.move + move, curr_node.price + price, curr_node )
        if state in nodes:
            if nodes[state].price > price + curr_node.price:
                n = nodes[state]
                n.move, n.price, n.father = curr_node.move + [move], curr_node.price + price, curr_node
        else:
          new_node = Node(state, curr_node.move + [move], curr_node.price + price, curr_node)
          data_struct.push(new_node)
          nodes[state] = new_node

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  return search(problem, util.Queue())

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  return search(problem, util.PriorityQueueWithFunction(lambda node: node.price))


def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  return search(problem, util.PriorityQueueWithFunction(lambda node: node.price + heuristic(node.position, problem)))
  
'''----------------Heuristics--------------'''
def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def manhattanHeuristic(position, problem, info={}):
  "The Manhattan distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
  "The Euclidean distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5



# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

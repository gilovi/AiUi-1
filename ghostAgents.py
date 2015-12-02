# ghostAgents.py 
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
import search


class CatsSearchProblem(search.SearchProblem):

  def __init__(self, gameState, goal=(1,1), start=None, costFn = lambda x: 1):
    """
    Stores the start and goal.

    gameState: A GameState object (pacman.py)
    costFn: A function from a search state (tuple) to a non-negative number
    goal: A position in the gameState
    """
    self.walls = gameState.getWalls()
    self.startState = start
    self.goal = goal
    self.costFn = costFn
    
  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
     return state == self.goal

  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.

     As noted in search.py:
         For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
    """
    # chasing = self.index - 1

    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )

    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999
    """
    if actions == None: return 999999
    x,y= self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
      cost += self.costFn((x,y))
    return cost

class CatAgent(Agent):
  MIN_DIST = 8
  origStart = None
  def __init__( self, index ,fn='aStarSearch', prob = CatsSearchProblem, heuristic='manhattanHeuristic' ):
    self.index = index
    heur = getattr(search, heuristic)
    func = getattr(search, fn)
    self.searchFunction = lambda x: func(x, heuristic=heur)
    self.searchType = prob


  def getAction( self, state ):
    if self.origStart == None: self.origStart = state.getGhostPosition(self.index)
    chased = self.index % (state.getNumAgents() - 1) + 1
    chasing = self.index - 1
    if chasing == 0 : chasing =  state.getNumAgents() - 1
    
    #if manhattanDistance(state.getGhost(chasing), state.getGhost(self.index)) < MIN_DIST
    #   return max(dist, action for dist in state.getLegalActions(self.index))
    problem = self.searchType(state, state.getGhostPosition(chased),
         state.getGhostPosition(self.index))
    if len(self.searchFunction(problem)) == 0:
      print("@@@ ghosts colide ghostIndex=" + str(self.index) + " @@@")

      # deColideProblem = self.searchType(state, self.origStart)
      return  Directions.STOP #deColideProblem
    return self.searchFunction(problem)[0]

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    #if len(dist) == 0:
      #return Directions.STOP
    #else:
    return util.chooseFromDistribution( dist )

  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
      
  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    else:
      bestScore = min( distancesToPacman )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
    
    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
    dist.normalize()
    return dist





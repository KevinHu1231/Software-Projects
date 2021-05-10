#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    goal = state.destination
    locations = state.snowballs

    dist = 0
    for x in locations:
        idx = locations[x]
        if idx == 0 or idx == 1 or idx == 2:
            dist = dist + abs(x[0] - goal[0]) + abs(x[1] - goal[1])
        elif idx == 3 or idx == 4 or idx == 5:
            dist = dist + 2*(abs(x[0] - goal[0]) + abs(x[1] - goal[1]))
        elif idx == 6:
            dist = dist + 3*(abs(x[0] - goal[0]) + abs(x[1] - goal[1]))

    return dist

#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)


def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    #Uses the manhattan distance heuristic but also adds more features. Heuristic sets a score of infinity to unsolvable positions.
    #For example, if a snowball is right next to a boundary of the board and the destination is not right next to the same boundary,
    #or if snowball is right next two obstacles in two non-opposing cardinal directions ie. (one obstacle to the left, one obstacle on top).
    #Heuristic also adds a constant penalty of 2 or 4 to the distance (best value found during testing) for incorrect snowball structures at the goal.
    #Heuristic also slightly discourages snowballs being next to walls by adding a constant penalty of 1 to the distance if the snowball is next to a wall.
    #The last two features mentioned and their penalty values were found to be optimal during testing.

    dist = 0 #Intialize parameters
    height = state.height - 1
    width = state.width - 1

    for x in state.snowballs: #Loop through all snowball structures

        idx = state.snowballs[x] #Determine type of snowball structure

        #If a snowball is along a wall and the goal is not along the wall, the problem can't be solved.

        if (x[0] == 0) and (state.destination[0] != 0):
            return float("inf")
        if (x[1] == 0) and (state.destination[1] != 0):
            return float("inf")
        if (x[0] == width) and (state.destination[0] != width):
            return float("inf")
        if (x[1] == height) and (state.destination[1] != height):
            return float("inf")

        #If a snowball is next to two obstacles in two non-opposing cardinal direction, the problem can't be solved.

        if(x[0]+1, x[1]) in state.obstacles and (x[0], x[1]+1) in state.obstacles:
            return float("inf")
        elif(x[0]-1, x[1]) in state.obstacles and (x[0], x[1]-1) in state.obstacles:
            return float("inf")
        elif(x[0]+1, x[1]) in state.obstacles and (x[0], x[1]-1) in state.obstacles:
            return float("inf")
        elif(x[0]-1, x[1]) in state.obstacles and (x[0], x[1]+1) in state.obstacles:
            return float("inf")

        #Adds a constant distance penalty of 1 if the snowball structure is next to a wall

        if (x[0]+1, x[1]) in state.obstacles or (x[0]-1, x[1]) in state.obstacles or (x[0], x[1]+1) in state.obstacles or (x[0], x[1]-1) in state.obstacles:
            dist += 1

        if x == state.destination:
            penalty = 2 #Penalty is to penalize wrong snowball structures at the goal
        else:
            penalty = 0

        #Manhattan distance with penalty, penalties are only for incorrect snowball structures at the goal, incomplete structures are not penalized
        if idx==0:
            dist += abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) #No penalty for large snowball at goal
        elif idx==1:
            dist += abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) + penalty #Penalties for medium and small snowball at goal
        elif idx==2:
            dist += abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) + penalty
        elif idx==3:
            dist += 2 * abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) #No penalty for large and medium snowball at goal
        elif idx==4:
            dist += 2 * abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) + 2*penalty #Two times penalty for medium and small snowball at goal since both snowballs need to be removed
        elif idx==5:
            dist += 2 * abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) + penalty #Penalty for large and small snowball at goal
        elif idx==6:
            dist += 3 * abs(x[0] - state.destination[0]) + abs(x[1] - state.destination[1]) #No penalty for snowman at goal

    return dist

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return sN.gval + (weight * sN.hval)

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  #'''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  #'''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  #'''OUTPUT: A goal state (if a goal is found), else False'''
  #'''implementation of weighted astar algorithm'''

    time = os.times()[0] #Start timing after function is called

    wrapped_fval_function = (lambda sN: fval_function(sN,weight)) #Initialize search parameters
    se = SearchEngine('custom','full')
    se.init_search(initial_state, snowman_goal_state, heur_fn, wrapped_fval_function)
    time_left = timebound

    time_left -= os.times()[0] - time #Update leftover time after initializing search

    res = se.search(time_left) #Initialize best result and cost after first search
    best_res = res
    best_cost = (float("inf"), float("inf"), float("inf"))

    while 1: #Loop until time runs out

        if res == False: #Return best result when search fails to find a better path in time limit
            return best_res

        #Check if path needs to be updated or pruned
        if res.gval <= best_cost[0]:
            best_res = res
            best_cost = (res.gval,res.gval,res.gval)

        time_left -= os.times()[0] - time  # Update leftover time to find better path
        time = os.times()[0] #Start timing again
        weight -= 0.01 #Update weight (This decrement value was found to be optimal during testing)
        res = se.search(time_left,best_cost) #Keep searching

def anytime_gbfs(initial_state, heur_fn, timebound = 5):
    #IMPLEMENT
    #'''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    #'''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    #'''OUTPUT: A goal state (if a goal is found), else False'''
    #'''implementation of gbfs algorithm'''

    time = os.times()[0] #Start timing after function is called

    se = SearchEngine('best_first','full') #Initialize search parameters
    se.init_search(initial_state, snowman_goal_state, heur_fn)
    time_left = timebound

    time_left -= os.times()[0] - time #Update leftover time after initializing search

    res = se.search(time_left) #Initialize best result and cost after first search
    best_res = res
    best_cost = (float("inf"), float("inf"), float("inf"))

    while 1:  # Loop until time runs out

        if res == False:  # Return best result when search fails to find a better path in time limit
            return best_res

        # Check if path needs to be updated or pruned
        if res.gval <= best_cost[0]:
            best_res = res
            best_cost = (res.gval, res.gval , res.gval)

        time_left -= os.times()[0] - time  # Update leftover time to find better path
        time = os.times()[0]  # Start timing again

        res = se.search(time_left, best_cost)  # Keep searching
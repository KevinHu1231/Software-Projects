"""
An AI player for Othello.

Performance: My heuristic stays under the 10 second timeout for depth 6 and board size 8 and below. For depth 7 and
board size 8, most moves stay under the 10 second timeout by some moves may take up to 30 seconds. This only applies
for the alpha beta algorithm with caching and ordering.

Description of My Heuristic: My heuristic depends on 7 different parameters, each with different weights. The parameter
weights are overridden in some special cases however. The heuristic gives a value of infinity if the AI can win the
game, ie. the AI has more points when a player has no legal moves, and gives a value of negative infinity if the AI
will lose the game, ie. the AI has less points when a player has no legal moves. The 7 parameters are dependent on the
number of corners owned, the number of x squares owned, the number of c squares owned, the current mobility, the
potential mobility, the stability of the position and the coin parity. A x-square is a square that is one square
diagonal to a corner. A c-square is a square that is one square vertical or horizontal to a corner. In my definition,
these squares only count if the adjacent corner is not owned by the same player. Since corners are very valuable and
you may risk losing a corner by placing on these squares, these squares have negative weights. The corners themselves
have high positive weights. The current mobility is just the number of moves a player has which has small positive
weight. The potential mobility is similar but considers future moves more, and thus has a larger positive weight. The
potential mobility tracks the number of pieces a player has that has an empty square adjacent to it. The stability is
the number of pieces a player has that cannot be flipped back, and this has a high positive weight. Finally, the coin
parity is the same as the compute utility heuristic, the number of pieces a player has. The coin parity has a dynamic
weight. The weight is an exponential function of the number of pieces on the board over the number of squares on the
board. The dynamic weight ensures that the number of pieces is a lot more important closer to the end of the game,
assuming that the game does not end early. Each of these parameters are converted into positive and negative fractions
before multiplying by their associated weight. The fractions follow the formula given below:
(my_parameter - opp_parameter) / (my_parameter + opp_parameter)
My_parameter refers to the parameter applied to the player being evaluated on, and opp_parameter refers to the parameter
applied to the opposing player. Note that if my_parameter + opp_parameter = 0, the formula just gives zero instead.
The final heuristic score is the weighted sum of the fractions of the different parameters. The heuristic can easily
be improved by optimizing the values of the weights, or even having different sets of weights for different board sizes.
"""

import random
import sys
import time
import math

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

#Dictionary for caching
cache_dict = dict()

def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    # IMPLEMENT
    p1, p2 = get_score(board)
    if color == 1:
        val = p1 - p2
    elif color == 2:
        val = p2 - p1
    else:
        return False
    return val  # change this!


# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional

    num_1, num_2 = get_score(board)
    #Determines which pieces are for the player being evaluated on (my) and which pieces are for the opponent (opp).
    if color == 1:
        my_color = 1
        my_pieces = num_1
        opp_color = 2
        opp_pieces = num_2
    else:
        my_color = 2
        my_pieces = num_2
        opp_color = 1
        opp_pieces = num_1

    #Determines my current mobility and the opponent's current mobility
    my_current_mobility = len(get_possible_moves(board, my_color))
    opp_current_mobility = len(get_possible_moves(board, opp_color))

    #Heuristic returns infinity if the player can win, has more points when a player has no legal moves left,
    #negative infinity if the opposing player has more points when a player has no legal moves left.
    if my_current_mobility == 0 or opp_current_mobility == 0:
        if my_pieces>opp_pieces:
            return float("inf")
        else:
            return float("-inf")

    size = len(board) - 1

    #Determines number of my corners, x squares and c squares.
    my_corners = 0
    my_x_squares = 0
    my_c_squares = 0

    if board[0][0] == my_color:
        my_corners += 1
    else:
        if board[1][1] == my_color:
            my_x_squares += 1
        if board[0][1] == my_color:
            my_c_squares += 1
        if board[1][0] == my_color:
            my_c_squares += 1

    if board[0][size] == my_color:
        my_corners += 1
    else:
        if board[1][size-1] == my_color:
            my_x_squares += 1
        if board[1][size] == my_color:
            my_c_squares += 1
        if board[0][size-1] == my_color:
            my_c_squares += 1

    if board[size][0] == my_color:
        my_corners += 1
    else:
        if board[size-1][1] == my_color:
            my_x_squares += 1
        if board[size-1][0] == my_color:
            my_c_squares += 1
        if board[size][1] == my_color:
            my_c_squares += 1

    if board[size][size] == my_color:
        my_corners += 1
    else:
        if board[size-1][size-1] == my_color:
            my_x_squares += 1
        if board[size-1][size] == my_color:
            my_c_squares += 1
        if board[size][size-1] == my_color:
            my_c_squares += 1

    # Determines number of the opponent's corners, x squares and c squares.
    opp_corners = 0
    opp_x_squares = 0
    opp_c_squares = 0

    if board[0][0] == opp_color:
        opp_corners += 1
    else:
        if board[1][1] == opp_color:
            opp_x_squares += 1
        if board[0][1] == opp_color:
            opp_c_squares += 1
        if board[1][0] == opp_color:
            opp_c_squares += 1

    if board[0][size] == opp_color:
        opp_corners += 1
    else:
        if board[1][size - 1] == opp_color:
            opp_x_squares += 1
        if board[1][size] == opp_color:
            opp_c_squares += 1
        if board[0][size - 1] == opp_color:
            opp_c_squares += 1

    if board[size][0] == opp_color:
        opp_corners += 1
    else:
        if board[size - 1][1] == opp_color:
            opp_x_squares += 1
        if board[size - 1][0] == opp_color:
            opp_c_squares += 1
        if board[size][1] == opp_color:
            opp_c_squares += 1

    if board[size][size] == opp_color:
        opp_corners += 1
    else:
        if board[size - 1][size - 1] == opp_color:
            opp_x_squares += 1
        if board[size - 1][size] == opp_color:
            opp_c_squares += 1
        if board[size][size - 1] == opp_color:
            opp_c_squares += 1

    my_potential_mobility = 0
    opp_potential_mobility = 0

    my_stability = 0
    opp_stability = 0

    #Loops through entire board

    for i in range(0,size+1):
        for j in range(0,size+1):

            #Determines my stability

            #The way stability is determined for a particular piece is that there is a path to the edge of the board
            #consisting entirely of pieces of that colour in all four directions, vertically, horizontally and
            #both diagonals. The diagonal from top left to bottom right is called diagonal and the diagonal from bottom
            #left to top right is called antidiagonal. This way there is no way two opposing pieces can sandwich
            #the piece since one side is touching the edge of the board.

            if board[i][j] == my_color:

                #Stability
                while 1:
                    #Vertical
                    #Is there a vertical path to the edge of the board? If not, piece is not stable.
                    tf = True
                    for x in range(0,i):
                        if board[x][j] != my_color:
                            tf = False
                            break
                    if not tf:
                        tf = True
                        for x in range(i+1,size+1):
                            if board[x][j] != my_color:
                                tf = False
                                break
                    if not tf:
                        break
                    #Horizontal
                    # Is there a horizontal path to the edge of the board? If not, piece is not stable.
                    for x in range(0, j):
                        if board[i][x] != my_color:
                            tf = False
                            break
                    if not tf:
                        tf = True
                        for x in range(j + 1, size + 1):
                            if board[i][x] != my_color:
                                tf = False
                                break
                    if not tf:
                        break

                    #Diagonal
                    # Is there a diagonal path to the edge of the board? If not, piece is not stable.
                    lower_limit = min(i,j)
                    upper_limit = min(size-i,size-j)

                    for x in range(0, lower_limit):
                        if board[i-x][j-x] != my_color:
                            tf = False
                            break

                    if not tf:
                        tf = True
                        for x in range(0, upper_limit):
                            if board[i+x][j+x] != my_color:
                                tf = False
                                break
                    if not tf:
                        break

                    #Antidiagonal
                    # Is there an anti-diagonal path to the edge of the board? If not, piece is not stable.
                    lower_limit = min(size-i, j)
                    upper_limit = min(i,size-j)

                    for x in range(0, lower_limit):
                        if board[i+x][j-x] != my_color:
                            tf = False
                            break

                    if not tf:
                        tf = True
                        for x in range(0, upper_limit):
                            if board[i-x][j+x] != my_color:
                                tf = False
                                break

                    #If paths to the edge of the board in all four directions exist, piece is stable.
                    if tf:
                        my_stability += 1

                    break


                #Potential Mobility
                #Determines my potential mobility

                #Check if any of the spots surrounding the piece are out of bounds. If so, don't check these spots.
                if i - 1 >= 0:
                    up = 1
                else:
                    up = 0
                if j - 1 >= 0:
                    left = 1
                else:
                    left = 0
                if i + 1 <= size:
                    down = 1
                else:
                    down = 0
                if j + 1 <= size:
                    right = 1
                else:
                    right = 0

                #Check all valid squares surrounding the piece

                if up == 1:
                    if board[i-1][j] == 0:
                        my_potential_mobility += 1
                if down == 1:
                    if board[i+1][j] == 0:
                        my_potential_mobility += 1
                if left == 1:
                    if board[i][j-1] == 0:
                        my_potential_mobility += 1
                if right == 1:
                    if board[i][j+1] == 0:
                        my_potential_mobility += 1

                if up == 1 and left == 1:
                    if board[i-1][j-1] == 0:
                        my_potential_mobility += 1
                if up == 1 and right == 1:
                    if board[i-1][j+1] == 0:
                        my_potential_mobility += 1
                if down == 1 and left == 1:
                    if board[i+1][j-1] == 0:
                        my_potential_mobility += 1
                if down == 1 and right == 1:
                    if board[i+1][j+1] == 0:
                        my_potential_mobility += 1

            #Calculates stability and potential mobility for the opponent. All code is pretty much the same except
            #use opp instead of my.

            if board[i][j] == opp_color:
                #Stability
                while 1:
                    # Vertical
                    tf = True
                    for x in range(0, i):
                        if board[x][j] != opp_color:
                            tf = False
                            break
                    if not tf:
                        tf = True
                        for x in range(i + 1, size + 1):
                            if board[x][j] != opp_color:
                                tf = False
                                break
                    if not tf:
                        break
                    # Horizontal
                    for x in range(0, j):
                        if board[i][x] != opp_color:
                            tf = False
                            break
                    if not tf:
                        tf = True
                        for x in range(j + 1, size + 1):
                            if board[i][x] != opp_color:
                                tf = False
                                break
                    if not tf:
                        break

                    # Diagonal
                    lower_limit = min(i, j)
                    upper_limit = min(size - i, size - j)

                    for x in range(0, lower_limit):
                        if board[i - x][j - x] != opp_color:
                            tf = False
                            break

                    if not tf:
                        tf = True
                        for x in range(0, upper_limit):
                            if board[i + x][j + x] != opp_color:
                                tf = False
                                break
                    if not tf:
                        break

                    # Antidiagonal
                    lower_limit = min(size - i, j)
                    upper_limit = min(i, size - j)

                    for x in range(0, lower_limit):
                        if board[i + x][j - x] != opp_color:
                            tf = False
                            break

                    if not tf:
                        tf = True
                        for x in range(0, upper_limit):
                            if board[i - x][j + x] != opp_color:
                                tf = False
                                break
                    if tf:
                        opp_stability += 1

                    break

                #Potential Mobility
                if i - 1 >= 0:
                    up = 1
                else:
                    up = 0
                if j - 1 >= 0:
                    left = 1
                else:
                    left = 0
                if i + 1 <= size:
                    down = 1
                else:
                    down = 0
                if j + 1 <= size:
                    right = 1
                else:
                    right = 0

                if up == 1:
                    if board[i - 1][j] == 0:
                        opp_potential_mobility += 1
                if down == 1:
                    if board[i + 1][j] == 0:
                        opp_potential_mobility += 1
                if left == 1:
                    if board[i][j - 1] == 0:
                        opp_potential_mobility += 1
                if right == 1:
                    if board[i][j + 1] == 0:
                        opp_potential_mobility += 1

                if up == 1 and left == 1:
                    if board[i - 1][j - 1] == 0:
                        opp_potential_mobility += 1
                if up == 1 and right == 1:
                    if board[i - 1][j + 1] == 0:
                        opp_potential_mobility += 1
                if down == 1 and left == 1:
                    if board[i + 1][j - 1] == 0:
                        opp_potential_mobility += 1
                if down == 1 and right == 1:
                    if board[i + 1][j + 1] == 0:
                        opp_potential_mobility += 1

    #Calculates the fractional values of the parameters or gives 0 if my_parameter + opp_parameter = 0
    if my_corners+opp_corners == 0:
        corner_percentage = 0
    else:
        corner_percentage = (my_corners-opp_corners)/(my_corners+opp_corners)

    if my_x_squares+opp_x_squares == 0:
        x_square_percentage = 0
    else:
        x_square_percentage = (my_x_squares-opp_x_squares)/(my_x_squares+opp_x_squares)

    if my_c_squares+opp_c_squares == 0:
        c_square_percentage = 0
    else:
        c_square_percentage = (my_c_squares-opp_c_squares)/(my_c_squares+opp_c_squares)

    if my_current_mobility+opp_current_mobility == 0:
        current_mobility_percentage = 0
    else:
        current_mobility_percentage = (my_current_mobility-opp_current_mobility)/(my_current_mobility+opp_current_mobility)

    if my_potential_mobility+opp_potential_mobility == 0:
        potential_mobility_percentage = 0
    else:
        potential_mobility_percentage = (my_potential_mobility-opp_potential_mobility)/(my_potential_mobility+opp_potential_mobility)

    if my_stability+opp_stability == 0:
        stability_percentage = 0
    else:
        stability_percentage = (my_stability-opp_stability)/(my_stability+opp_stability)

    #Calculates dynamic weight for coin parity fraction based on an exponential function of number of pieces over
    #number of spaces on the board.

    if my_pieces+opp_pieces == 0:
        coin_parity = 0
        coin_parity_weight = 1
    else:
        coin_parity = (my_pieces-opp_pieces)/(my_pieces+opp_pieces)

        #7 is the base weight for the dynamic coin parity weight, which can be change for further optimization.

        coin_parity_weight = 7**((my_pieces+opp_pieces)/(size**2))

    #Returns weighted sum of the parameter fractions. The weights can be further optimized to create a better AI.

    # IMPLEMENT
    return 10*corner_percentage + -8*x_square_percentage + -5*c_square_percentage + 3*current_mobility_percentage + 5*potential_mobility_percentage + 15*stability_percentage + coin_parity_weight*coin_parity
  # change this!


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching=0):
    # IMPLEMENT (and replace the line below)

    #Check if minimax value is in cache
    if caching == 1:
        if board in cache_dict.keys():
            return cache_dict[(board, color)]

    moves = get_possible_moves(board, 3-color)

    #If no legal moves or depth limit reached return utility
    if (moves == []) or (limit == 0):
        result = (None, compute_utility(board, color))
        return result

    value = float('inf')
    best_move = moves[0]

    #Recursion
    for move in moves:
        nxt_pos = play_move(board, 3-color, move[0], move[1])
        nxt_val = minimax_max_node(nxt_pos, color, limit - 1, caching)[1]
        if value > nxt_val:
            value, best_move = nxt_val, move

    #Store minimax value in cache
    if caching == 1:
        cache_dict[(board, color)] = (best_move, value)

    return (best_move, value)


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    # IMPLEMENT (and replace the line below)

    # Check if minimax value is in cache
    if caching == 1:
        if (board, color) in cache_dict.keys():
            return cache_dict[(board, color)]

    moves = get_possible_moves(board, color)
    # If no legal moves or depth limit reached return utility
    if (moves == []) or (limit == 0):
        result = (None, compute_utility(board, color))
        return result

    value = float('-inf')
    best_move = moves[0]

    #Recursion
    for move in moves:
        nxt_pos = play_move(board, color, move[0], move[1])
        nxt_val = minimax_min_node(nxt_pos, color, limit - 1, caching)[1]
        if value < nxt_val:
            value, best_move = nxt_val, move

    # Store minimax value in cache
    if caching == 1:
        cache_dict[(board, color)] = (best_move, value)

    return (best_move, value)


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    #Check if limits are valid and call max node
    if (type(limit) == int) and (limit > 0):
        lim = limit
        best_move, value = minimax_max_node(board, color, lim, caching)
    else:
        lim = float("inf")
        best_move, value = minimax_max_node(board, color, lim, caching)
    return best_move

    # IMPLEMENT (and replace the line below)


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT (and replace the line below)

    #Check if result is in the cache
    if caching == 1:
        if (board, color) in cache_dict.keys():
            return cache_dict[(board, color)]

    moves = get_possible_moves(board, 3-color)

    # If no legal moves or depth limit reached return utility
    if (moves == []) or (limit == 0):
        result = (None, compute_utility(board, color))

        return result

    value = float('inf')
    best_move = moves[0]

    #Store move and new board state into a list of tuples
    nxt_poses = []
    for move in moves:
        new_pos = play_move(board, 3-color, move[0], move[1])
        nxt_poses += [(move, new_pos)]

    #For ordering sort by the utility value of the board state resulting from the move
    if ordering == 1:
        nxt_poses.sort(key=lambda x: compute_utility(x[1], color), reverse=False)

    #Recursion and alpha beta pruning checks
    for nxt_pos in nxt_poses:
        nxt_val = alphabeta_max_node(nxt_pos[1], color, alpha, beta, limit - 1, caching, ordering)[1]
        if value > nxt_val:
            value, best_move = nxt_val, nxt_pos[0]
        if value <= alpha:
            return (best_move, value)
        beta = min(beta, value)

    #Store the result of alpha beta into cache
    if caching == 1:
        cache_dict[(board, color)] = (best_move, value)

    return (best_move, value)


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT (and replace the line below)

    # Check if result is in the cache
    if caching == 1:
        if (board, color) in cache_dict.keys():
            return cache_dict[(board, color)]

    moves = get_possible_moves(board, color)

    # If no legal moves or depth limit reached return utility
    if (moves == []) or (limit == 0):
        result = (None, compute_utility(board, color))
        return result

    value = float('-inf')
    best_move = moves[0]

    #Store move and new board state into a list of tuples
    nxt_poses = []
    for move in moves:
        new_pos = play_move(board, color, move[0], move[1])
        nxt_poses += [(move, new_pos)]

    #For ordering sort by the utility value of the board state resulting from the move
    if ordering == 1:
        nxt_poses.sort(key=lambda x: compute_utility(x[1], color), reverse=True)

    #Recursion and alpha beta pruning checks
    for nxt_pos in nxt_poses:
        nxt_val = alphabeta_min_node(nxt_pos[1], color, alpha, beta, limit - 1, caching, ordering)[1]
        if value < nxt_val:
            value, best_move = nxt_val, nxt_pos[0]
        if value >= beta:
            return (best_move, value)
        alpha = max(alpha, value)

    #Store the result of alpha beta into cache
    if caching == 1:
        cache_dict[(board, color)] = (best_move, value)

    return (best_move, value)


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """

    #Check if limits are valid and call the max node
    if (type(limit) == int) and (limit > 0):
        lim = limit
        best_move, value = alphabeta_max_node(board, color, float("-inf"), float("inf"), lim, caching, ordering)
    else:
        lim = float("inf")
        best_move, value = alphabeta_max_node(board, color, float("-inf"), float("inf"), lim, caching, ordering)

    return best_move

    # IMPLEMENT (and replace the line below)


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            board = tuple(tuple(row) for row in board)
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()

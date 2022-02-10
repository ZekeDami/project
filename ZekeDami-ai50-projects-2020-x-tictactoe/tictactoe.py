"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # at initial state X get the move
    if board == initial_state():
        return X

    num_of_x = 0
    num_of_o = 0
    for i in board:
        for j in i:
            if j == X:
                num_of_x += 1
            elif j == O:
                num_of_o += 1

    if num_of_x > num_of_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    avialable_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                avialable_actions.add((i, j))

    return avialable_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    p = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = p

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check for horizontal winner

    for i in range(3):
        numval_x = 0
        numval_o = 0
        for j in range(3):
            if board[i][j] == X:
                numval_x += 1
            if board[i][j] == O:
                numval_o += 1
        if numval_x == 3:
            return X
        if numval_o == 3:
            return O

    # check for vertical winner
    for i in range(3):
        numval1_x = 0
        numval1_o = 0
        for j in range(3):
            if board[j][i] == X:
                numval1_x += 1
            if board[j][i] == O:
                numval1_o += 1
        if numval1_x == 3:
            return X
        if numval1_o == 3:
            return O



    # check for vertical winner
    diagonals = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
    for diagonal in diagonals:
        numval2_x = 0
        numval2_o = 0
        for i, j in diagonal:
            if board[i][j] == X:
                numval2_x += 1
            if board[i][j] == O:
                numval2_o += 1
        if numval2_x == 3:
            return X
        if numval2_o == 3:
            return O

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = winner(board)
    if util == X:
        return 1
    elif util == O:
        return -1

    return 0


def mini_val(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_val(result(board, action)))
    return v


def max_val(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, mini_val(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if board == initial_state():
        return (random.randint(0, 2), random.randint(0, 2))
    play = player(board)
    action_to_take = None
    if play == X:
        val = -math.inf
        for action in actions(board):
            val1 = mini_val(result(board, action))
            if val < val1:
                val = val1
                action_to_take = action
        return action_to_take
    if play == O:
        val = math.inf
        for action in actions(board):
            val2 = max_val(result(board, action))
            if val > val2:
                val = val2
                action_to_take = action
        return action_to_take

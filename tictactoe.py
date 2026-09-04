"""
Tic Tac Toe Player
"""

import math

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
    countX = sum(row.count(X) for row in board)
    countO = sum(row.count(O) for row in board)

    if countX == countO:
        return X
    else:
        return O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(0,3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise Exception("Action out of bounds")
    if board[i][j] is not EMPTY:
        raise Exception("Invalid action")
    new_board = [row[:] for row in board]
    if player(board) == X:
        new_board[i][j] = X
    else:
        new_board[i][j] = O
    return new_board
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0, 3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
        
    if terminal(board):
        return None
    
    if player(board) == X:
        best_score = -math.inf
        best_action = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
        return best_action
    else:
        best_score = math.inf
        best_action = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action
        return best_action

def max_value(board):
    if terminal(board):
        return utility(board)
    best_score = -math.inf
    for action in actions(board):
        score = min_value(result(board, action))
        best_score = max(best_score, score)
    return best_score

def min_value(board):
    if terminal(board):
        return utility(board)
    best_score = math.inf
    for action in actions(board):
        score = max_value(result(board, action))
        best_score = min(best_score, score)
    return best_score
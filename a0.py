#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017

# Modified by Snehal Chemburkar Vartak 10 Sep 2017

# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

# Updated the code to solve both nrooks and nqueens based on the input parameters
# The unavailable tile is accounted for in this code
# Used numpy array to calculate the # of rooks or queens along each diagonal

import sys
import numpy as np


# Count # of pieces in given row
def count_on_row(board, row):
    return sum(board[row])

# Count # of pieces in given column
def count_on_col(board, col):
    return sum([row[col] for row in board])

# Count total # of pieces on board
def count_pieces(board):
    return sum([sum(row) for row in board])

# Added code to calculate the diagonals
# Count # of pieces in each diagonal of 2D numpy array
def count_np_diag(board):
    sum_each_diagonal = []
#### FOLLOWING LINES OF CODE ARE ADAPTED FROM - https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
    for i in range(N-1,-N,-1):
        sum_each_diagonal.append(np.sum(np.asarray(board).diagonal(i)))
	
    for j in range(-N+1,N):
        sum_each_diagonal.append(np.sum(np.asarray(board)[::-1,:].diagonal(j)))
#### END CODE QUOTATION      
    return sum_each_diagonal
        
# Return a string with the board rendered in a human-friendly format
# Modified by Snehal Vartak to reflect the unavailable tile 
def printable_board(board):
    return "\n".join([" ".join(["X" if col == (y-1) and row == (x-1) else "R" if board[row][col]==1 else "_" for col in range(0,N)]) for row in range(0,N)])

def printable_queens_board(board):
    return "\n".join([" ".join(["X" if col == (y-1) and row == (x-1) else "Q" if board[row][col]==1 else "_" for col in range(0,N)]) for row in range(0,N)])


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1, ] + board[row][col + 1:]] + board[row + 1:]

# Get list of successors of given board state where total number of queens 
# at any time is less than or equal to N and successors with no new moves are removed.
# Modified the successors2() for nqueens to remove the states where the diagonals had more than one queen.- Snehal Vartak  
def successors_queens(board):
    succ_list_queens = []
    
    for r in range(0,N):
        if count_on_row(board,r) == 1:
            continue
        for c in range(0,N):
            if count_on_col(board,c)==1 or (r == x-1 and c==y-1):
                continue
            interim_board = add_piece(board,r,c)
            if count_pieces(interim_board) <= N and interim_board != board:
                diagonals = count_np_diag(interim_board)
                if all([diagonals[i] <=1 for i in range(0,len(diagonals))]):
                    succ_list_queens.append(interim_board)
        return succ_list_queens

# Successor function for nrooks from my nrooks.py submission
# Get list of successors of given board state where total number of 
# rooks at any time is less than or equal to N and successors with no new moves are removed.
def successors2(board):
    succ_list = []
    
    for r in range(0,N):
        if count_on_row(board,r) == 1:
            continue
        for c in range(0,N):
            if count_on_col(board,c)== 1 or (r == x-1 and c==y-1):
                continue
            interim_board = add_piece(board,r,c)
            if count_pieces(interim_board) <= N and interim_board != board:
                succ_list.append(interim_board)
    return succ_list
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
            all([count_on_row(board,r) == 1 for r in range(0,N)]) and \
            all([count_on_col(board,c) == 1 for c in range(0,N)])


# Solve n-queens!
def solve_queens(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors_queens(fringe.pop()):
            if is_goal(s):
                return (s)
            fringe.append(s)
    return False

# Solve n-rooks!
def solve_rooks(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2(fringe.pop()):
            if is_goal(s):
                return (s)
            fringe.append(s)
    return False

if len(sys.argv) != 5:
    print ("Please pass 4 arguments:\n 1: nrook or nqueen \n 2: size of the board, N \
           \n 3: x coordinate of unavailable tile \n 4: y coordinate of unavailable tile.")
else:
    # Decide which code to run based on input argument:
    code_to_run = str(sys.argv[1])
    
    # This is N, the size of the board. It is passed through command line arguments.
    N = int(sys.argv[2])
    
    #    Define x and y as the row and column co-ordinates for the unavailable square
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    
    # The board is stored as a list-of-lists. Each inner list is a row of the board.
    # A zero in a given square indicates no piece, and a 1 indicates a piece.
    initial_board = [[0] * N] * N
    
    
    if code_to_run == "nqueen":
        print ("Starting from initial board:\n" + printable_queens_board(initial_board) + "\n\nLooking for solution...\n")
        solution_queens = solve_queens(initial_board)
        print (printable_queens_board(solution_queens) if solution_queens else "Sorry, no solution found. :(")
    elif code_to_run == "nrook":
        print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
        solution_rooks = solve_rooks(initial_board)
        print (printable_board(solution_rooks) if solution_rooks else "Sorry, no solution found. :(")
    else:
        print ("Please pass proper arguments!")

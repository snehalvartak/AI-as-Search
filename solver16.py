#!/usr/bin/env python

# (1) Abstraction
# The state space for this problem will include all possible combinations of 1-15 and blank title on the board

# The Successor Function will consist of states where one, two or three tiles shifted either left,right, up or down in one move.
# So each state will have upto 9 successor states.

# The evaluation function f(s) = g(s) + h(s) is formulated as, 
# g(s) is the number of moves to reach state s, the cost for one move is one
# h(s) - For solving the N-puzzle with 1 tile shift in one move, Manhattan distance is 
# the better heuristic compared to the number of misplaced tiles. In this problem, 
# we are allowed to shift one, two or three tiles in one move. Thus, in this case 
# a maximum of 3 mispalced tiles can be rectified in one move. This relaxation makes the
# manhattan distance not admissible since it overestimates the number of moves required to reach the goal state.
# We relax the heuristic to calculate manhattan distance divided by 3,to account for the fact that a maximum of
# 3 tiles can be placed in their correct position in one move.
# For this problem, the heuristic Manhattan distance divided by 3 will always be admissible.

# (2) How the search algorithm works

# I have defined a class Node to store the node state, its corresponding g(s) -- cost to reach that state from the initial state,
# h(s) is the minimum number of moves required to reach the goal state from current state, 
# f(s) = g(s) + h(s), and the path taken to reach that state

# The initial state is read from the input file
# The goal state has been defined in the code.
# The a star search function solve() will be initialized with the initial state from the board, g(s) = 0 and path =[]
# from there we check if this state is the goal state, if not we look for the successors and add the current node to a visited dict
# For each successor we check if the successor is the goal state, if so we quit and return the Node object path.
# If the successor if not a goal state, we check if it has not been visited. If it has not been visited we add it to the fringe 
# along with it total cost f(s) which acts as its priority.
# We maintain the visited dictionary with the nodes already expanded to reduce computations.

# (3) Problems faced -
# Earlier used heapq implementation of priority queue
# as data structure for the fringe. But for a 15puzzle with 15 steps to the goal state, took around 45 minutes to find the 
# minimal cost path. 
# It was not possible to easily change the priority of an already existing item in the heapq.
# After changing my code to use priority queue form Queue, the code returns the optimal response much faster.
# This also facilitated updating the priority of an item in the fringe to a lower cost.
# if we try to check if a successor state exists in the fringe previously, the computations take too long to process
# the code works much faster without that check.
# found it much simpler to use Priority Queue compared to heapq.

import sys
import numpy as np
from Queue import PriorityQueue
from copy import deepcopy
#sys.setrecursionlimit(10000) 

#Initialize direction variable variables
shift = ['L','R','U','D']
#Initialize the goal index to hold the coordinates for the goal state
goal_index={}
    
    
# Creating an object to store all the values related to the state of the board
# such as the board state, it cost to reach that state, heuristic , path at that state

# Referred the best way to store multiple values for a state from http://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/
class Node:
    def __init__(self, node,cost,path):
        self.node_state = node
        self.cost_of_move = cost
        self.total_cost = self.cost_of_move + self.heuristic_2(self.node_state)
        self.path = path
        
    # Second Heuristic  - Sum of manhattan distance of each number from its goal state
    def heuristic_2(self,node_state):
        
        #First get the coordinated of each tile in the current board
        current_index={}
        for i in range(0,4):
            for j in range(0,4):
                if node_state[i][j] !=0:
                    current_index[node_state[i][j]] =[i,j]
        if len(goal_index) == 0:
            for i in range(0,4):
                for j in range(0,4):
                    if goal_state[i][j] != 0:
                        goal_index[goal_state[i][j]]=[i,j]
        man_dist = 0
        for k in goal_index:
            if k != 0:
                man_dist = man_dist + abs(current_index[k][0] - goal_index[k][0]) + abs(current_index[k][1] - goal_index[k][1])
        return man_dist/3
        

def successors(current_node):
    succ_nodes = []
    board =current_node.node_state
    cost = current_node.cost_of_move + 1 #For each successor of the previous state, the cost will be cost until previous state + 1
    
    #Get the row and col position of the blank tile on the board
    row = np.where(np.array(board)==0)[0][0]
    col = np.where(np.array(board)==0)[1][0]
    n = len(board) - 1 - col #Number of possible shifts horizontally
    m = len(board) - 1 - row #Number of possible shifts vertically
    #Based on the position of the blank tile, we will move the numbered tiles left, right, up and down
    for s in shift:
        # Generate successors by shifting one, two or three numbered tiles left
        if n != 0 and s == 'L':
            for i in range(0,n):
                if i == 0:
                    board_1 = deepcopy(board)
                    board_1[row][col+i], board_1[row][col+1+i] = board_1[row][col+1+i], board_1[row][col+i]
                    path_1 = current_node.path[:]
                    path_1.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_1,cost,path_1))
                if i == 1:
                    board_2 = deepcopy(board_1)
                    board_2[row][col+i], board_2[row][col+1+i] = board_2[row][col+1+i], board_2[row][col+i]
                    path_2 = current_node.path[:]
                    path_2.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_2,cost,path_2))
            
                if i == 2:
                    board_3 = deepcopy(board_2)
                    board_3[row][col+i], board_3[row][col+1+i] = board_3[row][col+1+i], board_3[row][col+i]
                    path_3 = current_node.path[:]
                    path_3.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_3,cost,path_3))
        # Generate successors by shifting one, two or three numbered tiles right
        if n != 3 and s == 'R':
            for i in range(0,col):
                if i == 0:
                    board_4 = deepcopy(board)
                    board_4[row][col-i], board_4[row][col-1-i] = board_4[row][col-1-i], board_4[row][col-i]
                    path_4 = current_node.path[:]
                    path_4.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_4,cost,path_4))
                if i == 1:
                    board_5 = deepcopy(board_4)
                    board_5[row][col-i], board_5[row][col-1-i] = board_5[row][col-1-i], board_5[row][col-i]
                    path_5 = current_node.path[:]
                    path_5.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_5,cost,path_5))
                if i == 2:
                    board_6 = deepcopy(board_5)
                    board_6[row][col-i], board_6[row][col-1-i] = board_6[row][col-1-i], board_6[row][col-i]
                    path_6 = current_node.path[:]
                    path_6.append(''.join([s,str(i+1),str(row+1)]))
                    succ_nodes.append(Node(board_6,cost,path_6))
                   
        # Generate successors by shifting one, two or three numbered tiles up
        if m != 0 and s == 'U':
            for i in range(0,m):
                if i == 0:
                    board_7 = deepcopy(board)
                    board_7[row+i][col], board_7[row+i+1][col] = board_7[row+i+1][col], board_7[row+i][col]
                    path_7 = current_node.path[:]
                    path_7.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_7,cost,path_7))
                    
                if i == 1:
                    board_8 = deepcopy(board_7)
                    board_8[row+i][col], board_8[row+i+1][col] = board_8[row+i+1][col], board_8[row+i][col]
                    path_8 = current_node.path[:]
                    path_8.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_8,cost,path_8))
                if i == 2:
                    board_9 = deepcopy(board_8)
                    board_9[row+i][col], board_9[row+i+1][col] = board_9[row+i+1][col], board_9[row+i][col]
                    path_9 = current_node.path[:]
                    path_9.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_9,cost,path_9))
        # Generate successors by shifting one, two or three numbered tiles down
        if m != 3 and s == 'D':
            for i in range(0,row):
                if i == 0:
                    board_10 = deepcopy(board)
                    board_10[row-i][col], board_10[row-i-1][col] = board_10[row-i-1][col], board_10[row-i][col]
                    path_10 = current_node.path[:]
                    path_10.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_10,cost,path_10))
                if i == 1:
                    board_11 = deepcopy(board_10)
                    board_11[row-i][col], board_11[row-i-1][col] = board_11[row-i-1][col], board_11[row-i][col]
                    path_11 = current_node.path[:]
                    path_11.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_11,cost,path_11))
                if i == 2:
                    board_12 = deepcopy(board_11)
                    board_12[row-i][col], board_12[row-i-1][col] = board_12[row-i-1][col], board_12[row-i][col]    
                    path_12 = current_node.path[:]
                    path_12.append(''.join([s,str(i+1),str(col+1)]))
                    succ_nodes.append(Node(board_12,cost,path_12))
    return succ_nodes


# check if board is a goal state
def is_goal(board):
    if board.node_state == goal_state:
        return True
    else:
        return False

# Referred Pseudo Code for A-star from https://en.wikipedia.org/wiki/A*_search_algorithm 
# and http://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html
# Solve 16 puzzle
def solve(initial_node,goal_state):
    #for the initial state of the board, the cost function g is 0.
    #thus, the evaluation function is equal to the heuristic. i.e
    #initial cost of move is 0
    start_node = Node(initial_node,0,[])
    #Priority queue to get element with the lowest total cost
    fringe = PriorityQueue()
    fringe.put((start_node.total_cost,start_node))
    visited = {}
    
    while not fringe.empty():
        current = fringe.get()
        if current[1].node_state == goal_state:
            return (current[1].path)
        if str(current[1].node_state) in visited:
            continue
        list_successors = successors(current[1])
        visited[str(current[1].node_state)] = True
        for s in list_successors:
            #Check if the node is already visited
            if str(s.node_state) in visited:
                if visited[str(s.node_state)]:
                    continue
            if is_goal(s):
                return (s.path)
            
            if str(s.node_state) not in visited and s.node_state != initial_node:
                fringe.put((s.total_cost,s))

    return False



#We will check the parity of the initial board. If it is even then the puzzle is solvable, if it is odd
# it cannot be solved
def is_solvable(initial_board):
    #Get the elements in the matrix as a list while preserving the order of numbers
    board = np.array(initial_board).flatten()
    permutation_inversions = 0
    n = board.shape[0]
    
    for i in range(0,n):
        for j in range(i+1,n):
            if board[i]>board[j] and board[i]!=0 and board[j]!= 0:
                permutation_inversions +=1
    
    #Adding the row number of the empty tile
    zero_row = np.where(np.array(initial_state) == 0)[0][0] + 1 
    
    permutation_inversions = permutation_inversions + zero_row
    #print permutation_inversions
    # If parity of the initial board is odd the puzzle cannot be solved.
    if permutation_inversions%2 == 1:
        return False
    else:
        return True





 # Main Code
if len(sys.argv) != 2:
    print ("Please proper arguments")
else:
# Get the intial configuration on the board from the input file
    initial_state = []
    filename = str(sys.argv[1])
    print filename
    input_file = open(filename,"r")
       # A zero in a given square indicates no piece
    initial_state = [[int(num) for num in line.split()] for line in input_file.readlines()]
    input_file.close()
    
    goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    
    if is_solvable(initial_state):
        solution = solve(initial_state,goal_state)
        if solution:
            print "Solution Found"
            print " ".join(solution)
        else:
            print "No Solution"
       
    else:
        print "Given board has odd parity, hence it cannot be solved."

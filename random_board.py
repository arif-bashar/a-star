"""
author: Arif Bashar
CSCI 4350 OLA1

Use random actions to generate random starting
states for the 8-puzzle problem
"""

import sys, random
      
# Moves 0 up if it can
def moveUp(xpos, ypos, board):
    if xpos == 0:
        return xpos, ypos, board
    board[xpos][ypos] = board[xpos-1][ypos]
    xpos -= 1
    board[xpos][ypos] = 0
    return xpos, ypos, board

# Moves 0 down if it can
def moveDown(xpos, ypos, board):
    if xpos == 2:
        return xpos, ypos, board
    board[xpos][ypos] = board[xpos+1][ypos]
    xpos += 1
    board[xpos][ypos] = 0
    return xpos, ypos, board
    
# Moves 0 left if it can
def moveLeft(xpos, ypos, board):
    if ypos == 0:
        return xpos, ypos, board
    board[xpos][ypos] = board[xpos][ypos-1]
    ypos -= 1
    board[xpos][ypos] = 0
    return xpos, ypos, board
    
# Moves 0 right if it can
def moveRight(xpos, ypos, board):
    if ypos == 2:
        return xpos, ypos, board
    board[xpos][ypos] = board[xpos][ypos+1]
    ypos += 1
    board[xpos][ypos] = 0
    return xpos, ypos, board

def printBoard(board):
    for line in board:
        print(str(line).strip('[]').replace(',', ''))
    
def main():
    # Grab command line args
    random.seed(int(sys.argv[1]))
    moveNum = int(sys.argv[2])
    
    # Game board
    board = []

    # Read from standard input into 2D list
    for line in sys.stdin.readlines():
        board.append([])
        for i in line.strip().split(' '):
            board[-1].append(int(i))
    
    # We know where the 0 is in the goal state
    xpos, ypos = 0, 0
                
    # Does a random move moveNum times
    for i in range(moveNum):
        # Numbers 0-4 correspond to direction
        rMove = random.randrange(4)
        if rMove == 0:
            xpos, ypos, board = moveUp(xpos, ypos, board)
        elif rMove == 1:
            xpos, ypos, board = moveDown(xpos, ypos, board)
        elif rMove == 2:
            xpos, ypos, board = moveLeft(xpos, ypos, board)
        elif rMove == 3:
            xpos, ypos, board = moveRight(xpos, ypos, board)
    
    printBoard(board)
    
main()

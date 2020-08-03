"""
author: Arif Bashar

Take in a randomly generated 8 puzzle board
and solve it using the A* Search algorithm
"""

import sys, heapq, copy

# Global variables
heuristic = int(sys.argv[1])
goal = [[0,1,2],[3,4,5],[6,7,8]]
nodeid = 0

# What we'll use for the frontier
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

# What we'll use for the closed list
class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet

# What we'll use to instantiate states
class state():
    def __init__(self, xpos, ypos, board):
        self.xpos = xpos
        self.ypos = ypos
        self.tiles = board
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

# Node class to implement into our search
class node():
    def __init__(self,val,level,state,parent=None):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.val = val
        self.level = level
        self.state = state
        self.parent = parent
    def __str__(self):
        return 'Node: id=%d val=%d level=%d'%(self.id,self.val, self.level)

# Main f function
def f(n):
    if n.state == None:
        return None
    else:
        return g(n) + h(n)

# Cost function
def g(n):
    return n.level

# Heuristic function
def h(n):
    if heuristic == 0:
        return 0
    if heuristic == 1:
        return tilesDisplaced(n.state.tiles)
    if heuristic == 2:
        return manhattan(n.state.tiles)
    if heuristic == 3:
        return novelH(n.state.tiles)

# Calculate # of tiles displaced heuristic
def tilesDisplaced(board):
    displaced = 0
    for x in range(3):
        for y in range(3):
            if board[x][y] != goal[x][y]:
                displaced += 1
    return displaced

# Calculate manhattan distance heuristic
def manhattan(board):
    distance = 0
    for i in range(1,9):
        x1, y1 = getXY(board, i)
        x2, y2 = getXY(goal, i)
        distance += abs(x2-x1) + abs(y2-y1)
    return distance

# Return x and y of game board
def getXY(board,i):
    for x in range(3):
        for y in range(3):
            if (board[x][y] == i):
                return x, y

# Custom heuristic
def novelH(board):
    # Sum of each row in goal state
    goalR1, goalR2, goalR3 = 3, 12, 21
    
    # Initialize sums for current state
    boardR1, boardR2, boardR3 = 0, 0, 0
    
    for x in range(3):
        for y in range(3):
            if x == 0:
                boardR1 += board[x][y]
            if x == 1:
                boardR2 += board[x][y]
            if x == 2:
                boardR3 += board[x][y]
                
    # Get the difference in the rows of current
    # board and goal state
    boardR1 = abs(boardR1 - goalR1)
    boardR2 = abs(boardR2 - goalR2)
    boardR3 = abs(boardR3 - goalR3)
    
    # Return sum of the differences
    return boardR1+boardR2+boardR3

# Generate children
def genChildren(parent):
    
    """ There's definitely a better way to write
    this function, but we'll work with it for now """
    
    pState = parent.state
    level = parent.level + 1  # Cost is just level of node
    
    # Declare all the new states and call the corresponding moves
    up = state(pState.xpos, pState.ypos, pState.tiles)
    up = up.up()
    down = state(pState.xpos, pState.ypos, pState.tiles)
    down = down.down()
    left = state(pState.xpos, pState.ypos, pState.tiles)
    left = left.left()
    right = state(pState.xpos, pState.ypos, pState.tiles)
    right = right.right()
    
    # Declare the new nodes with temp val
    upNode = node(0, level, up, parent)
    downNode = node(0, level, down, parent)
    leftNode = node(0, level, left, parent)
    rightNode = node(0, level, right, parent)
    
    # Re-set their values
    upNode.val = f(upNode)
    downNode.val = f(downNode)
    leftNode.val = f(leftNode)
    rightNode.val = f(rightNode)

    # Throw them into a list and return
    childrenList = [upNode, downNode, leftNode, rightNode]
    return childrenList

# Just return the x and y val of where the 0 is
def findZero(board):
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                return x, y
    return None

def main():
    board = []    # Game board
    frontier = PriorityQueue()    # Que for frontier
    closedSet = Set()    # Set for closed (list)
    path = [] # Finding the path
    
    # Read from standard input into 2D list
    for line in sys.stdin.readlines():
        board.append([])
        for i in line.strip().split(' '):
            board[-1].append(int(i))
    
    # We need to find the x and y position of the zero
    xpos, ypos = findZero(board)
    
    # Initialization
    initialState = state(xpos, ypos, board)
    root = node(0, 0, initialState)
    root.value = f(root)
    frontier.push(root)
    
    # Actual A* Algorithm
    while not frontier.isEmpty():
        current = frontier.pop()
        if current.state.tiles == goal:
            break
        closedSet.add(current.state)
        children = genChildren(current)
        for child in children:
            if not child.state == None and not closedSet.isMember(child.state):
                frontier.push(child)
                
    d = current.level

    if (d == 0):
        b = 0
    else:
        b = pow(closedSet.length()+frontier.length(),1/d)
        
    print("V=",closedSet.length(),sep='')
    print("N=",closedSet.length()+frontier.length(),sep='')
    print("d=",d,sep='')
    print("b=",b,"\n",sep='')
    
    while (current != None):
        path.append(current.state.tiles)
        current = current.parent
        
    path.reverse()
    
    for x in path:
        for line in x:
            print(str(line).strip('[]').replace(',', ''))
        print("\n")
    
main()
"""
15 Puzzles

"""

import sys
import string
import heapq
import itertools
from random import randint
from random import shuffle
from collections import deque
import time

#------------------------------------------------
# Board settings

directions = ['N','S','W','E']
maxnodes = 50000
maxdepth = 20
maxtraindep = 18

N = 15
board_size = 4

loops = list(itertools.product(range(board_size), range(board_size)))

#------------------------------------------------
# Class definitions

class State:
    offsets = { "N": (-1,  0),
                "S": ( 1,  0),
                "W": ( 0, -1),
                "E": ( 0,  1)}

    def at(self,r,c):
        return (self.coding>>((r*4+c)*4)) & N

    def set(self, r, c, v):
        self.coding |= (v<<((r*4+c)*4))

    def clear(self,r,c):
        self.coding &= ~(N<<((r*4+c)*4))

    # return the coding with all tiles not in the pattern masked
    def mask(self, pattern):
        masked = self.coding
        for r,c in loops:
            if self.at(r,c) not in pattern:
                masked &= ~(N<<((r*4+c)*4))
        return masked
        
    def __init__(self, coding, blank, parent=None, action=None, cost=0):
        self.coding = coding
        self.blank = blank
        self.parent = parent
        self.action = action
        self.cost = cost
            
    def swap(self, row, col, ro, co):
        self.blank = (row+ro,col+co)
        self.set(row,col,self.at(row+ro,col+co))
        self.clear(row+ro,col+co)

    def move(self, direction, cost=1):
        row, col = self.blank
        ro, co = State.offsets[direction]
        if row+ro >= 0 and row+ro < board_size and col+co >= 0 and col+co < board_size:       
            child = State(self.coding,self.blank,self,direction,self.cost+cost)
            child.swap(row,col,ro,co)
            return child
        else:
            return None      

    def trace(self):
        steps = []
        node = self
        while node.parent:
            steps.append(node.action)
            node = node.parent
        return steps
            
    def win(self, goal):        
        return self.coding == goal.coding

    def __hash__(self):
        return hash(self.coding) # hash(blank), depends on which one is faster
        
    def __eq__(self, other):
        return self.blank==other.blank and self.coding==other.coding
    
    def __str__(self):
        string = "-------------------\n"
        for r in range(board_size):
            for c in range(board_size):
                string += ("%4d" % self.at(r, c))
            string += "\n"
        string += "-------------------\n"
        return string

def h_none(state1, state2):
    return 0

def uniform_cost(action):
    return 1

def zero_cost(action):
    return 0

def h_manhattan(state1, state2):
    pos1 = [0] * 16
    pos2 = [0] * 16        
        
    for r,c in loops:
        pos1[state1.at(r,c)] = (r,c)
        pos2[state2.at(r,c)] = (r,c)

    pos1[0] = pos2[0] = (0,0)
    dist = sum([abs(x[0]-y[0])+abs(x[1]-y[1]) for x,y in zip(pos1, pos2)])
    return dist

class PatternDB:
    def __init__(self, pattern):
        self.pattern = pattern
        self.cache = {}

    def search(self, state):
        code = state.mask(self.pattern)
        return self.cache.get(code, 0)

    def add(self, state, steps):
        code = state.mask(self.pattern)
        if code not in self.cache:
            self.cache[code] = steps

            
patterns = [[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15]]
#patterns = [[x] for x in range(1,16)] # train manhattan

class PatternState(State):
    def __init__(self, coding, blank, steps=0, parent=None, action=None, cost=0):
        self.steps = steps
        State.__init__(self,coding, blank, parent, action, cost)        
        
    def move(self, direction, cost=1):
        row, col = self.blank
        ro, co = State.offsets[direction]
        
        if row+ro >= 0 and row+ro < board_size and col+co >= 0 and col+co < board_size:       
            child = PatternState(self.coding,self.blank,self.steps,self,direction,self.cost+cost)
            child.swap(row,col,ro,co)
            v = child.at(row,col)
            if v != 0: child.steps += 1
            return child
        else:
            return None          

def train_pattern(goal, pattern):
    db = PatternDB(pattern)
    goal = PatternState(goal.coding, goal.blank)
    goal.coding = goal.mask(pattern)
    frontier = deque() # FIFO queue
    visited = set()
    visited.add((goal.coding, goal.blank))
    frontier.append(goal)
    i = 0
    while frontier:
        current = frontier.popleft()
        db.add(current, current.steps)        
        
        if current.cost > maxtraindep: break
        
        for direction in directions:
            child = current.move(direction)
            if not child: continue

            if (child.coding,child.blank) not in visited:
                frontier.append(child)
                visited.add((child.coding, child.blank))
        i += 1
        if i == 2:
            print("--------------------- OPEN")
            print([node.coding for node in frontier])
            print("--------------------- CLOSED")
            print(visited)
    return db

import re
def parse_state(statestr):
    statestr.strip('"\'')
    statestr = statestr[1:-1] # remove parenthesis
    rowsstr = re.findall('\(.*?\)', statestr)    
    blank = tuple(map(int, rowsstr[-1][1:-1].split(' ')))
    rows = [map(int, row[1:-1].split(' ')) for row in rowsstr[0:-1]]

    state = State(0L,blank)
    for r,c in loops:
        state.set(r,c,rows[r][c])
    return state

pdbs = []        
def train(goal):
    for pattern in patterns:
        pdbs.append(train_pattern(goal, pattern))

def h_patterndb(state, goal):
    h = sum([pdb.search(state) for pdb in pdbs])
    return max(h, h_manhattan(state,goal))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python puzzle.py <start-state> <goal-state>"
        sys.exit(1)
    start = parse_state(sys.argv[1])
    goal = parse_state(sys.argv[2])

    print "Training patterns: maximum training depth is %d" % maxtraindep
    # print "Cutoff depth for DFS and IDFS is %d" % maxdepth
    # print "Cutoff nodes visited for uniform/greedy/astar search is %d" % maxnodes

    t = time.clock()
    train(goal)
    print "Training time: ", time.clock() - t, " cpu seconds"

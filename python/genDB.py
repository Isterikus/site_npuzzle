from collections import deque
from json import dump
from time import clock
from itertools import product

import CONSTANTS
CONSTANTS.board_size = 4
CONSTANTS.N = pow(CONSTANTS.board_size, 2) - 1
CONSTANTS.loops = list(product(range(CONSTANTS.board_size), range(CONSTANTS.board_size)))
from Node2 import Node

directions = ['N','S','W','E']
maxtraindep = 18
patterns = [[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15]]

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


class PatternState(Node):
	def __init__(self, coding, blank, steps=0, parent=None, action=None, cost=0):
		self.steps = steps
		Node.__init__(self,coding, blank, parent, action, cost)        

	def move(self, direction, cost=1):
		row, col = self.blank
		ro, co = Node.offsets[direction]

		if row + ro >= 0 and row+ro < board_size and col + co >= 0 and col+co < board_size:
			child = PatternState(self.coding, self.blank, self.steps, self.direction, self.cost+cost)
			child.swap(row, col, ro, co)
			v = child.at(row, col)
			if v != 0:
				child.steps += 1
			return child
		else:
			return None


def train_pattern(goal, pattern):
	db = PatternDB(pattern)
	goal = PatternState(goal.coding, goal.blank)
	goal.coding = goal.mask(pattern)
	frontier = deque()  # FIFO queue
	visited = set()
	visited.add((goal.coding, goal.blank))
	frontier.append(goal)
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
	return db


def parse_state(statestr):
	state = Node(0,(3,3))
	for r,c in loops:
		state.set(r,c,statestr[r][c])
	return state


pdbs = []


def train(goal):
	for pattern in patterns:
		pdbs.append(train_pattern(goal, pattern))


if __name__ == "__main__":
	goal = parse_state([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
	print(goal)
	print("Training patterns: maximum training depth is %d" % maxtraindep)

	t = clock()
	train(goal)
	print("Training time: ", clock() - t, " cpu seconds")
	i = 0
	for i in range(2):
		if i == 0:
			file = "DATABASE_7_8-1"
		else:
			file = "DATABASE_7_8-2"
		with open("../databases/" + file, 'w') as out:
			print("CACHE LEN = ", len(pdbs[i].cache))
			dump(pdbs[i].cache, out)

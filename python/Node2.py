# import test
from itertools import product

board_size = 4
N = pow(board_size, 2) - 1
loops = list(product(range(board_size), range(board_size)))

class Node:
	offsets = {"N": (-1,  0),
				"S": ( 1,  0),
				"W": ( 0, -1),
				"E": ( 0,  1)}

	def at(self, r, c):
		return (self.coding >> ((r * 4 + c) * 4)) & N

	def set(self, r, c, v):
		self.coding |= (v << ((r * 4 + c) * 4))

	def clear(self,r,c):
		self.coding &= ~(N << ((r * 4 + c) * 4))

	# return the coding with all tiles not in the pattern masked
	def mask(self, pattern):
		masked = self.coding
		for r, c in loops:
			if self.at(r, c) not in pattern:
				masked &= ~(N << ((r * 4 + c) * 4))
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
		ro, co = Node.offsets[direction]
		if row+ro >= 0 and row+ro < board_size and col+co >= 0 and col+co < board_size:       
			child = Node(self.coding,self.blank,self,direction,self.cost+cost)
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


def parse_state(statestr):
	state = Node(0, (3, 3))
	for r, c in loops:
		state.set(r, c, statestr[r][c])
	return state


goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
goal = parse_state(goal)
print(goal.coding)

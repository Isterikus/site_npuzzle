from collections import deque
from time import clock
from json import dump

from Node import Node

from Heuristics import *
from Algorithms import get_snake

size = 4
all_cells = pow(size, 2)
# patterns = [[1, 2, 3, 5, 6], [4, 7, 8, 11, 12], [9, 10, 13, 14, 15]] # 5-5-5 2
# patterns = [[1, 2, 3, 12, 13], [4, 14, 5, 15, 6], [11, 10, 9, 8, 7]]
patterns = [[1, 2, 3, 5, 6], [4, 7, 8, 11, 12], [9, 13, 14, 15, 0]]
pdbs = []

to_move = -1
to_remember = -1


def check_not_in(node, arr):
	for el in arr:
		if el.field == node.field:
			return False
	return True


max_train_dep = 50


class PatternDB:
	def __init__(self, pattern):
		self.pattern = pattern
		self.cache = {}

	def search(self, state):
		code = state.mask(self.pattern)
		return self.cache.get(code, 0)

	def add(self, state):
		code = state.code(self.pattern, to_move, to_remember)
		if code not in self.cache:
			self.cache[code] = state.getG()


def train_pattern(goal, pattern, heu):
	db = PatternDB(pattern)
	frontier = deque()  # FIFO queue
	visited = set()
	visited.add((goal.code(pattern, heu.what_to_move, to_remember), heu.getZero(goal.field)))
	frontier.append(goal)
	while frontier:
		current = frontier.popleft()
		db.add(current)

		for child in current.getChildrens(heu):
			child.setParent(current)
			child_zero = heu.getZero(child.field)
			if current.field[child_zero] in pattern:
				child.setG(current.getG() + 1)
			else:
				child.setG(current.getG())
			child_code = child.code(pattern, heu.what_to_move, to_remember)
			if (child_code, child_zero) not in visited:
				frontier.append(child)
				visited.add((child_code, child_zero))
	return db


def train():
	goal = [i + 1 for i in range(pow(size, 2) - 1)]
	goal.append(0)
	snake = get_snake(size)
	to_move = goal[snake.index(0)]
	to_remember = snake[goal.index(0)]
	goal = Node(goal, size)
	heu = Heuristics(['manhattan'], size, to_move, to_remember)
	for pattern in patterns:
		pdbs.append(train_pattern(goal, pattern, heu))
		print("DB CACHED")


if __name__ == '__main__':
	t = clock()
	train()
	print("Training time: ", clock() - t, " cpu seconds")
	for i in range(len(patterns)):
		file = "DATABASE_5_5_5-" + str(i + 1)
		with open("../databases/" + file, 'w') as out:
			print("CACHE LEN = ", len(pdbs[i].cache))
			dump(pdbs[i].cache, out)

from collections import deque
from time import clock
from json import dump

from Node import Node

size = 4
all_cells = pow(size, 2)
patterns = [[1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]]
pdbs = []


def check_not_in(node, arr):
	for el in arr:
		if el.field == node.field:
			return False
	return True


max_train_dep = 18


class PatternDB:
	def __init__(self, pattern):
		self.pattern = pattern
		self.cache = {}

	def search(self, state):
		code = state.mask(self.pattern)
		return self.cache.get(code, 0)

	def add(self, state):
		code = state.code(self.pattern)
		if code not in self.cache:
			self.cache[code] = state.getG()


# class PatternState(Node):
# 	def __init__(self, coding, blank, steps=0, parent=None, action=None, cost=0):
# 		self.steps = steps
# 		Node.__init__(self,coding, blank, parent, action, cost)
#
# 	def move(self, direction, cost=1):
# 		row, col = self.blank
# 		ro, co = Node.offsets[direction]
#
# 		if row + ro >= 0 and row+ro < board_size and col + co >= 0 and col+co < board_size:
# 			child = PatternState(self.coding, self.blank, self.steps, self.direction, self.cost+cost)
# 			child.swap(row,col,ro,co)
# 			v = child.at(row,col)
# 			if v != 0: child.steps += 1
# 			return child
# 		else:
# 			return None


def train_pattern(goal, pattern):
	db = PatternDB(pattern)
	# goal = PatternState(goal.code(pattern), goal.getZero())
	# goal.coding = goal.mask(pattern)
	frontier = deque()  # FIFO queue
	visited = set()
	visited.add((goal.code(pattern), goal.getZero()))
	frontier.append(goal)
	while frontier:
		current = frontier.popleft()
		db.add(current)

		if current.getG() > max_train_dep: break

		for child in current.getChildrens():
			child.setParent(current)
			child_zero = child.getZero()
			if current.field[child_zero] in pattern:
				child.setG(current.getG() + 1)
			else:
				child.setG(current.getG())
			child_code = child.code(pattern)
			if (child_code, child_zero) not in visited:
				frontier.append(child)
				visited.add((child_code, child_zero))
	return db


def train():
	goal = [i + 1 for i in range(pow(size, 2) - 1)]
	goal.append(0)
	goal = Node(goal, size)
	for pattern in patterns:
		pdbs.append(train_pattern(goal, pattern))
		print("DB CACHED")


# def generate(databases):
# 	dbs = []
# 	for db in databases:
# 		dab = Node(db, size)
# 		rez = bfs(dab)
# 		print("1 DONE")
# 		dbs.append(rez)
# 		print(rez)


if __name__ == '__main__':
	t = clock()
	train()
	print("Training time: ", clock() - t, " cpu seconds")
	for i in range(2):
		if i == 0:
			file = "DATABASE_7_8-1"
		else:
			file = "DATABASE_7_8-2"
		with open("../databases/" + file, 'w') as out:
			print("CACHE LEN = ", len(pdbs[i].cache))
			dump(pdbs[i].cache, out)

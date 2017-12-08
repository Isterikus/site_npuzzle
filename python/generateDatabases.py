import collections

from Node import *

size = 4
all_cells = pow(size, 2)
database_6_6_3 = {'file': "database_6_6_3", 'db': [[1,2,3,-1,5,6,-1,-1,9,10,-1,-1,-1,-1,-1,0],[-1,-1,-1,4,-1,-1,7,8,-1,-1,11,12,-1,-1,-1,0],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,14,15,0]]}
# database_5_5_5 = {'file': "database_5_5_5", 'db': [[1,2,3,5,6,9],[4,7,8,11,12],[10,13,14,15]]}
# database_7_8 = {'file': "database_7-8", 'db': [[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15]]}

def check_not_in(node, arr):
	for el in arr:
		if el.field == node.field:
			return False
	return True
maxtraindep = 18
class patternDatabase():
	def __init__(self, pattern):
		self.pattern = pattern
		self.cache = {}

	def getPosition(self, val):
		for i in range(all_cells):
			if self.pattern.field[i] == val:
				return i
		return -1

	def hash(self, field):
		i = 0
		index = 0
		for val in field:
			position = self.getPosition(val)
			if (position != -1):
				index |= i << (position << 2)
			i += 1
		return index

	def addNode(self, node):
		h = self.hash(node.field)
		if h not in self.cache:
			self.cache[h] = node.getG()
		else:
			if self.cache[h] > node.getG():
				self.cache[h] = node.getG()

def bfs(initial):
	print(initial)
	db = patternDatabase(initial)
	visited, queque = [], collections.deque([initial])
	i = 0
	while queque:
		current = queque.popleft()
		db.addNode(current)
		if current.getG() > maxtraindep:
			break
		if i % 10 == 0:
			print(db.cache)
			# break
		i += 1
		for neighbor in current.getChildrens():
			neighbor.setParent(current)
			if neighbor.field not in visited:
				queque.append(neighbor)
				visited.append(neighbor.field)
	return db


def generate(databases):
	dbs = []
	for db in databases:
		dab = Node(db, size)
		rez = bfs(dab)
		print("1 DONE")
		dbs.append(rez)
		print(rez)

if __name__ == '__main__':
	generate(database_6_6_3['db'])
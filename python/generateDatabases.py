from collections import deque

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

maxtraindep = 11

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
			if (position > 0):
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

# def bfs(root):
# 	db = patternDatabase(root)
# 	visited, queue = set(), collections.deque([root])
# 	while queue:
# 		vertex = queue.popleft()
# 		db.addNode(vertex)
# 		if vertex.getG() > maxtraindep:
# 			break
# 		for neighbour in vertex.getChildrens():
# 			neighbour.setParent(vertex)
# 			if (neighbour.field) not in visited:
# 				visited.add((neighbour.field))
# 				queue.append(neighbour)
# 	return db

def bfs(pattern):
	db = patternDatabase(pattern)
	frontier = deque() # FIFO queue
	visited = set()
	visited.add((db.hash(pattern.field), pattern.getZero()))
	frontier.append(pattern)

	# i = 0
	while frontier:
		current = frontier.popleft()
		db.addNode(current)

		if current.getG() > maxtraindep:
			break
		# i += 1
		for child in current.getChildrens():
			child.setParent(current)
			h = db.hash(child.field)
			if (h,child.getZero()) not in visited:
				frontier.append(child)
				visited.add((h, child.getZero()))
		# if i == 1:
		# 	print("----------------------- CLOSED")
		# 	print(visited)
		# 	print("----------------------- OPEN")
		# 	print([db.hash(node.field) for node in frontier])
	return db

# def bfs(initial):
# 	visited, queque = set(), [initial]
# 	while queque:
# 		vertex = queque.pop(0)
# 		if vertex.getG() > maxtraindep:
# 			break
# 		if vertex.field not in [node.field for node in visited]:
# 			visited.add(vertex)
# 			for children in vertex.getChildrens():
# 				children.setParent(vertex)
# 				queque.append(children)
# 	return db


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
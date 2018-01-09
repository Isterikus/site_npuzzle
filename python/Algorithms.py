from time import time
from collections import deque
from .Heuristics import *
from .Node import *


class Algorithms():
	def __init__(self, algorithm, size, heuristics):
		self.goal = [i + 1 for i in range(pow(size, 2))]
		self.goal[pow(size, 2) - 1] = 0
		self.algorithm = algorithm
		self.size = size
		self.heuristics = Heuristics(heuristics, size)
	
	# IDA* START

	def depthFirstSearch(self, current, bound):
		if current.field == self.goal:
			return current
		for children in current.getChildrens():
			children.setParent(current)
			children.setG(current.getG() + 1)
			h = self.heuristics.getH(children)
			if children.getG() + h <= bound:
				rez = self.depthFirstSearch(children, bound)
				if rez != None:
					return rez
		return None

	def idaStar(self, startNode):
		bound = self.heuristics.getH(startNode)
		solution = None
		while solution == None:
			solution = self.depthFirstSearch(startNode, bound)
			bound += 2
		return solution

	# IDA* END

	def not_in(self, set, node):
		for temp in set:
			if node.field == temp.field:
				return False
		return True

	def aStar(self, startNode):
		closed = set()
		opened = list()
		opened.append(startNode)
		startNode.setH(self.heuristics.getH(startNode))
		while opened:
			curr = min(opened, key=lambda inst:inst.h)
			opened.remove(curr)
			if curr.field == self.goal:
				return curr
			closed.add("".join(map(str, curr.field)))
			for child in curr.getChildrens():
				if "".join(map(str, child.field)) not in closed:
					child.setParent(curr)
					child.setG(curr.getG() + 1)
					child.setH(self.heuristics.getH(child) + child.getG())
					if self.not_in(opened, child):
						opened.append(child)

	def bfs(self, startNode):
		opened = deque()
		closed = set()
		opened.append(startNode)
		while opened:
			current = opened.popleft()

			if current.field == self.goal:
				return current
			closed.add("".join(str(i) for i in current.field))
			for child in current.getChildrens():
				if "".join(str(i) for i in child.field) not in closed:
					child.setParent(current)
					if self.not_in(opened, child):
						opened.append(child)

	def solve(self, startField):
		sol = None
		startTime = time()
		startNode = Node(startField, self.size)
		if self.algorithm == "idaStar":
			sol = self.idaStar(startNode)
		elif self.algorithm == "aStar":
			sol = self.aStar(startNode)
		elif self.algorithm == "bfs":
			sol = self.bfs(startNode)
		return {'time': (time() - startTime), 'solution': sol}

# test = Algorithms("aStar", 3, "manhattan+linear2")

# 3
# 2 7 6
# 3 5 4
# 0 1 8

# test.solve(Node([2,7,6,3,5,4,0,1,8], 3))
# test.solve(Node([[1,2,3],[4,5,6],[7,0,8]], 3))

# Parallel Combinatorial Search  External-Memory Graph Search
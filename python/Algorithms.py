from time import time
from collections import deque
from .Heuristics import *
from .Node import *

class Algorithms():
	def __init__(self, algorithm, size, heuristics):
		self.goal = [i+1 for i in range(pow(size, 2))]
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
		startTime = time()
		while solution == None:
			solution = self.depthFirstSearch(startNode, bound)
			bound += 2
			# print("B=  ", bound)
		finish_time = time() - startTime
		print("PYTHON_IDA* TIME = ", finish_time)
		return {'time':finish_time,'solution':solution}

	# IDA* END

	def aStar(self, startNode):
		def not_in(set, node):
			for temp in set:
				if node.field == temp.field:
					return False
			return True

		startTime = time()
		closed = []
		opened = []
		opened.append(startNode)
		startNode.setH(self.heuristics.getH(startNode))
		while opened:
			curr = min(opened, key=lambda inst:inst.h)
			opened.remove(curr)
			# curr = opened.pop(0)
			if curr.field == self.goal:
				return {'time': (time() - startTime), 'solution': curr}
			closed.append(curr.field)
			for child in curr.getChildrens():
				if child.field not in closed:
					child.setParent(curr)
					child.setH(self.heuristics.getH(child))
					if not_in(opened, child):
						opened.append(child)

	def solve(self, startField):
		startNode = Node(startField, self.size)
		if self.algorithm == "idaStar":
			return self.idaStar(startNode)
		elif self.algorithm == "aStar":
			return self.aStar(startNode)

# test = Algorithms("aStar", 3, "manhattan+linear2")

# 3
# 2 7 6
# 3 5 4
# 0 1 8

# test.solve(Node([2,7,6,3,5,4,0,1,8], 3))
# test.solve(Node([[1,2,3],[4,5,6],[7,0,8]], 3))
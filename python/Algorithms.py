from time import time
from Heuristics import *
from Node import *

import multiprocessing

class Algorithms():
	def __init__(self, algorithm, size, heuristics):
		self.goal = [i+1 for i in range(pow(size, 2))]
		self.goal[pow(size, 2) - 1] = 0
		self.algorithm = algorithm
		self.size = size
		self.heuristics = Heuristics(heuristics, size)
		self.bound = 0
	
	# IDA* START

	def depthFirstSearch(self, current):
		threads = []
		if current.field == self.goal:
			return current
		childrens = current.getChildrens()
		i = 0
		while i < len(childrens):
			childrens[i].setParent(current)
			if childrens[i].getG() + self.heuristics.getH(childrens[i].field) > self.bound:
				del childrens[i]
			i += 1
		print(childrens)
		if len(childrens) == 0:
			return None
		print(childrens)
		p = multiprocessing.Pool()
		results = p.map(self.depthFirstSearch,[child for child in childrens])
		for rez in results:
			if rez != None:
				return rez
		p.close()
		p.join()
		'''
			rez = self.depthFirstSearch(children, bound)
			if rez != None:
				return rez
		'''
		return None

	def idaStar(self, startNode):
		self.bound = self.heuristics.getH(startNode.field)
		solution = None
		startTime = time()
		while solution == None:
			solution = self.depthFirstSearch(startNode)
			self.bound += 2
			print("B=  ", self.bound)
		finish_time = time() - startTime
		# print("PYTHON_IDA* TIME = ", finish_time)
		return {'time':finish_time,'solution':solution}

	# IDA* END

	def solve(self, startNode):
		if self.algorithm == "idaStar":
			return self.idaStar(startNode)

test = Algorithms("idaStar", 3, "manhattan+linear2")

# 3
# 2 7 6
# 3 5 4
# 0 1 8

test.solve(Node([2,7,6,3,5,4,0,1,8], 3))
# test.solve(Node([[1,2,3],[4,5,6],[7,0,8]], 3))
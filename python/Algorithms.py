from time import time
from Heuristics import *

class Algorithms():
	def __init__(self, algorithm, size, heuristics):
		self.goal = [[i+1 for i in range(j * size, j * size + size)] for j in range(size)]
		print(self.goal)
		self.algorithm = algorithm
		self.size = size
		self.heuristics = Heuristics(heuristics, size)
	
	# IDA* START

	def depthFirstSearch(current, bound):
		if current.field == self.goal:
			return current
		for children in current.getChildrens():
			pass

	def idaStar(self, startNode):
		bound = self.heuristics.getH(startNode.field)
		solution = None
		startTime = time.time()
		while solution == None:
			solution = depthFirstSearch(startNode, bound)
			bound += 2
		finish_time = time.time() - time
		print("PYTHON_ida* TIME = ", finish_time)
		return solution

	# IDA* END

	def solve(self, startNode):
		if self.algorithm == "idaStar":
			rez = self.idaStar(startNode)

test = Algorithms("idaStar", 4, "manhattan+linear")

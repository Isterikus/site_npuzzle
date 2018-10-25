from time import time
from collections import deque
import numpy as np
from .Heuristics import *
from .Node import *


def get_snake(n):
	way = 'r'
	arr = [[0 for _ in range(n)] for _ in range(n)]
	i = 0
	j = 0
	# count = 1
	go_to = n - 1
	ch_go_to = 3
	cou_go_to = 0
	passed_way = 0
	for count in range(1, n ** 2 + 1):
		arr[i][j] = count
		if count == n ** 2:
			arr[i][j] = 0
		# print(count, i, j, cou_go_to, go_to)
		count += 1
		if way == 'r':
			if passed_way == go_to:
				way = 'd'
				i += 1
				cou_go_to += 1
				passed_way = 1
			else:
				passed_way += 1
				j += 1
		elif way == 'd':
			if passed_way == go_to:
				way = 'l'
				j -= 1
				cou_go_to += 1
				passed_way = 1
			else:
				i += 1
				passed_way += 1
		elif way == 'l':
			if passed_way == go_to:
				way = 'u'
				i -= 1
				cou_go_to += 1
				passed_way = 1
			else:
				j -= 1
				passed_way += 1
		elif way =='u':
			if passed_way == go_to:
				way = 'r'
				j += 1
				cou_go_to += 1
				passed_way = 1
			else:
				i -= 1
				passed_way += 1
		if cou_go_to == ch_go_to:
			cou_go_to = 0
			go_to -= 1
			if ch_go_to == 3:
				ch_go_to = 2
	return [int(val) for val in np.array(arr).flatten()]


class Algorithms():
	def __init__(self, algorithm, size, heuristics):
		self.goal = [i + 1 for i in range(pow(size, 2))]
		self.goal[pow(size, 2) - 1] = 0
		self.algorithm = algorithm
		self.size = size
		self.heu = heuristics
		self.heuristics = None
		self.size_c = 1
		self.time_c = 1

	# IDA* START

	def depthFirstSearch(self, current, bound, g=0):
		if current.field == self.goal:
			self.size_c = g
			return current
		for children in current.getChildrens(self.heuristics):
			self.time_c += 1
			children.setParent(current)
			h = self.heuristics.getH(children)
			if g + h <= bound:
				rez = self.depthFirstSearch(children, bound, g + 1)
				if rez != None:
					return rez
		return None

	def idaStar(self, startNode):
		bound = self.heuristics.getH(startNode)
		print('bou', bound)
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
			if len(opened) > self.size:
				self.size_c = len(opened)
			curr = min(opened, key=lambda inst:inst.h)
			opened.remove(curr)
			if curr.field == self.goal:
				return curr
			closed.add("".join(map(str, curr.field)))
			for child in curr.getChildrens(self.heuristics):
				if "".join(map(str, child.field)) not in closed:
					child.setParent(curr)
					child.setG(curr.getG() + 1)
					child.setH(self.heuristics.getH(child) + child.getG())
					if self.not_in(opened, child):
						self.time_c += 1
						opened.append(child)

	def print_fie(self, field):
		k = 0
		for i in range(self.size):
			for j in range(self.size):
				print(field[k], end=" ")
				k += 1
			print("")
		print("----------------------------")

	def debag(self, set):
		for elem in set:
			self.print_fie(elem.field)

	def bfs(self, startNode):
		opened = deque()
		closed = set()
		opened.append(startNode)
		# i = 0
		while opened:
			if len(opened) > self.size:
				self.size_c = len(opened)
			current = opened.popleft()

			if current.field == self.goal:
				return current
			closed.add("".join(str(i) for i in current.field))
			for child in current.getChildrens(self.heuristics):
				if "".join(str(i) for i in child.field) not in closed:
					child.setParent(current)
					# if self.not_in(opened, child):
					self.time_c += 1
					opened.append(child)

	def solve(self, startField):
		snake_goal = get_snake(self.size)
		print(startField)
		new_start_field = [self.goal[snake_goal.index(val)] for val in startField]
		what_to_move = self.goal[snake_goal.index(0)]
		to_remember = snake_goal[self.goal.index(0)]
		self.heuristics = Heuristics(self.heu, self.size, what_to_move, to_remember)
		print(new_start_field)
		sol = None
		startTime = time()
		startNode = Node(new_start_field, self.size)
		if self.algorithm == "idaStar":
			sol = self.idaStar(startNode)
		elif self.algorithm == "aStar":
			sol = self.aStar(startNode)
		elif self.algorithm == "bfs":
			sol = self.bfs(startNode)
		# print("HEU Time = ", self.heu_time)
		return {'time': (time() - startTime), 'solution': sol, 'time_c': self.time_c, 'size_c': self.size_c}

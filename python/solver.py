# import numpy
import sys
import copy
import time
import math
from subprocess import call

n = 0
field_size = 0
field = []
goal = []
left_range = []
right_range = []
top_range = []
bottom_range = []

real_top_range = []
real_left_range = []

way = []

# DEFINE STATE CLASS
class State(object):
	# SRAV NA NORMI
	def __init__(self, field):
		self.field = field
		self.setH()

	def getH(self):
		return self.h

	def getG(self):
		try:
			return self.g
		except:
			self.g = self.parent.getG() + 1
			return self.g

	def getF(self):
		return self.g + self.h

	def setH(self):
		# self.h = self.getPatternDatabase() + self.getLinearConflictMine()
		self.h = self.getManhattan() + self.getLinearConflictMine()# + self.getOutOf()

	def setG(self, g):
		self.g = g

	def getParent(self):
		return self.parent

	def setParent(self, parent):
		self.parent = parent

	def getPatternDatabase(self):
		ret1 = 0
		ret2 = 0
		for i in range(n):
			for j in range(n):
				pos = i * n + j
				if (self.field[pos] == 0):
					continue
					pl_i = n - 1
					pl_j = n - 1
				elif self.field[pos] % n == 0:
					pl_i = self.field[pos] // n - 1
					pl_j = n - 1
				else:
					pl_i = self.field[pos] // n
					pl_j = self.field[pos] % n - 1
				if (self.field[pos] in real_top_range) or (self.field[pos] in real_left_range):
					ret1 += abs(i - pl_i) + abs(j - pl_j)
				else:
					ret2 += abs(i - pl_i) + abs(j - pl_j)
		return max(ret1, ret2)

	def getManhattan(self):
		ret = 0
		for i in range(n):
			for j in range(n):
				pos = i * n + j
				if (self.field[pos] == 0):
					pl_i = n - 1
					pl_j = n - 1
				elif self.field[pos] % n == 0:
					pl_i = self.field[pos] // n - 1
					pl_j = n - 1
				else:
					pl_i = self.field[pos] // n
					pl_j = self.field[pos] % n - 1
				# print('I = ', i, ' | J = ', j, ' | PL_I = ', pl_i, ' | PL_J = ', pl_j, ' | FIE = ', self.field[i * n + j], ' | REZ = ', abs(i - pl_i) + abs(j - pl_j))
				ret += abs(i - pl_i) + abs(j - pl_j)
		return ret

	# need to check
	def getEuclidean(self):
		ret = 0
		for i in range(n):
			for j in range(n):
				pl_i = self.field[i * n + j] // n
				pl_j = self.field[i * n + j] % n - 1
				ret += math.sqrt(math.pow(i - pl_i, 2) + math.pow(j - pl_j, 2))
		return ret

	def getLinearConflict(self):
		ret = 0
		for i in range(n):
			for j in range(n):
				pos = i * n + j
				if self.field[pos] != 0 and self.field[pos] % n == j + 1:
					for l in range(i, n):
						l_pos = l * n + j
						if self.field[l_pos] != 0 and self.field[l_pos] % n == j + 1:
							if self.field[pos] > self.field[l_pos]:
								ret += 2
				if self.field[pos] != 0 and (self.field[pos] - 1) // n == i:
					for k in range(j, n):
						k_pos = i * n + k
						if self.field[k_pos] != 0 and (self.field[k_pos] - 1) // n == i:
							if self.field[pos] > self.field[k_pos]:
								ret += 2
		return ret

	def getLinearConflictMine(self):
		ret = 0
		for i in range(n):
			for j in range(n):
				pos = i * n + j
				for l in range(i, n):
					l_pos = l * n + j
					if self.field[pos] > self.field[l_pos]:
						ret += 2
				for k in range(j, n):
					k_pos = i * n + k
					if self.field[pos] > self.field[k_pos]:
						ret += 2
		return ret

	def	getOutOf(self):
		ret = 0
		for i in range(n):
			for j in range(n):
				pl_i = self.field[i * n + j] // n
				pl_j = self.field[i * n + j] % n - 1
				if (pl_i != i):
					ret += 1
				if (pl_j != j):
					ret += 1
		return ret

	def findNeighbors(self):
		now = 0
		ret = []
		for i in range(field_size):
			if self.field[i] == 0:
				now = i
		if now not in left_range:
			tmp_field = copy.copy(self.field)
			tmp_field[now - 1], tmp_field[now] = tmp_field[now], tmp_field[now - 1]
			tmp_state = State(tmp_field)
			# print(tmp_field)
			ret.append(tmp_state)
		if now not in right_range:
			tmp_field = copy.copy(self.field)
			tmp_field[now + 1], tmp_field[now] = tmp_field[now], tmp_field[now + 1]
			tmp_state = State(tmp_field)
			ret.append(tmp_state)
		if now not in top_range:
			tmp_field = copy.copy(self.field)
			tmp_field[now - n], tmp_field[now] = tmp_field[now], tmp_field[now - n]
			tmp_state = State(tmp_field)
			# print_field(tmp_field, 0)
			ret.append(tmp_state)
		if now not in bottom_range:
			tmp_field = copy.copy(self.field)
			tmp_field[now + n], tmp_field[now] = tmp_field[now], tmp_field[now + n]
			tmp_state = State(tmp_field)
			ret.append(tmp_state)
		return ret

def print_field(fie, flag=1):
	if flag:
		print('---------------------------------------------------')
	for i in range(n):
		for j in range(n):
			sys.stdout.write(str(fie[i * n + j]) + ' ')
		sys.stdout.write('\n')


def checkInVisited(current):
	for state in visitedStates:
		if state.field == current.field:
			return True
	return False

def solveIDAStar():
	global newLimit
	global visitedStates
	limit = initialState.getH()
	result = None
	while result == None:
		visitedStates.append(initialState)
		newLimit = 1000000 # Fix this
		result = limitedSearch(initialState, limit)
		limit = newLimit
		# print('nL = ', newLimit)
		# if newLimit != 12:
			# exit()
		visitedStates = []
	return result

def wtf(field):
	j = 1
	for j in range(1, field_size):
		if field[j - 1] != j:
			return False
	if field[-1] != 0:
		return False
	return True

def limitedSearch(current, limit):
	global newLimit
	global best_solution
	global visitedStates
	for s in current.findNeighbors():
		# print_field(s.field)
		if wtf(s.field):
			s.setParent(current)
			return s
		if not checkInVisited(s):
			s.setG(current.getG() + 1)
			s.setParent(current)
			currentCost = s.getH() + s.getG()
			if currentCost <= limit:
				visitedStates.append(s)
				solution = limitedSearch(s, limit)
				if (solution != None) and (best_solution == None or solution.getG() < best_solution.getG()):
					best_solution = solution
			else:
				if currentCost < newLimit:
					newLimit = currentCost
	return None


def print_way(node):
	count = 0
	while node != None:
		print_field(node.field)
		node = node.getParent()
		count += 1
	print(count - 1)

def count_way(node):
	count = 0
	while node != None:
		pr

def search(node, g, bound):
	f = g + node.getH()
	if f > bound:
		return f
	if node.field == goal:
		# print_way(node)
		return 'FOUND'
	mn = 1000000
	for succ in node.findNeighbors():
		if node.getParent() and succ.field == node.getParent().field:
			continue
		succ.setParent(node)
		if g + 1 + succ.getH() <= bound:
			t = search(succ, g + 1, bound)
			if t == 'FOUND':
				return t
			if t < mn:
				mn = t
	return mn

def ida_star(initialState):
	bound = initialState.getH()
	rez_time = 0
	# print_field(initialState.field)
	start_time = time.time()
	# print("FIRST H = ", bound)
	while True:
		# print('BOUND = ', bound)
		t = search(initialState, 0, bound)
		# print("--- %s seconds ---" % (time.time() - start_time))
		if t == 'FOUND':
			rez_time = time.time() - start_time
			break
		bound += 2
		# print("B = ", bound)
	return rez_time

def solver(initial_field, main):
	initialState = State(initial_field)
	initialState.setG(0)
	initialState.setParent(None)
	if main:
		print_field(initialState.field)
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	to_c = ""
	for el in initialState.field:
		to_c += "," + str(el)
	to_c = to_c[1:]
	# print(to_c)
	# print('L = ', initialState.getLinearConflict())
	# exit()
	rez_time = ida_star(initialState)
	if main:
		print('PYTHON TIME: %s' % (rez_time))
		# call(["./a.out", str(n), to_c])
	return rez_time

def from_site(size, initial_field, main):
	global field_size, n, goal, left_range, right_range, top_range, bottom_range, real_top_range, real_left_range
	field_size = pow(size, 2)
	n = size
	goal = [i for i in range(1, field_size)]
	goal.append(0)
	left_range = [i * n for i in range(n)]
	right_range = [i * n - 1 for i in range(1, n + 1)]
	top_range = [i for i in range(n)]
	bottom_range = [i for i in range(field_size - n, field_size)]

	real_top_range = [i + 1 for i in top_range]
	real_left_range = [i + 1 for i in left_range]
	return solver(initial_field, main)

if __name__ == "__main__":
	n = 0
	field_size = 0
	field = []
	file = "npuzzle-3-5.txt"

	with open("../puzzles/" + file) as f:
		i = 0
		for line in f:
			if line[0] != '#' and not line[0].isdigit():
				print(line)
				error(1)
			elif line[0] == '#':
				pass
			elif n == 0:
				n = int(line)
				field_size = pow(n, 2)
				initial_field = [0 for s in range(field_size)]
			else:
				line = [s for s in line.split(' ') if s != '']
				for j in range(n):
					initial_field[i * n + j] = int(line[j])
				i += 1

	goal = [i for i in range(1, field_size)]
	goal.append(0)
	left_range = [i * n for i in range(n)]
	right_range = [i * n - 1 for i in range(1, n + 1)]
	top_range = [i for i in range(n)]
	bottom_range = [i for i in range(field_size - n, field_size)]

	real_top_range = [i + 1 for i in top_range]
	real_left_range = [i + 1 for i in left_range]
	solver(initial_field, True)

# from subprocess import call
from ctypes import *
from random import randint

from .Algorithms import *
from .generator import *
from .Node import *


import multiprocessing.pool
import functools

def timeout(max_timeout):
	"""Timeout decorator, parameter in seconds."""
	def timeout_decorator(item):
		"""Wrap the original function."""
		@functools.wraps(item)
		def func_wrapper(*args, **kwargs):
			"""Closure for function."""
			pool = multiprocessing.pool.ThreadPool(processes=1)
			async_result = pool.apply_async(item, args, kwargs)
			# raises a TimeoutError if execution exceeds max_timeout
			return async_result.get(max_timeout)
		return func_wrapper
	return timeout_decorator

def doRand(size):
	bem = [i + 1 for i in range(pow(size, 2))]
	bem[pow(size, 2) - 1] = 0
	goal = Node(bem, size)
	for _ in range(500):
		child = goal.getChildrens()
		i = randint(0, len(child) - 1)
		goal = child[i]
	return goal.field


def getRandomPath(size):
	path = []
	while True:
		# path = make_puzzle(size, False, 10000)
		path = doRand(size)
		bem = 0
		for i in range(pow(size, 2)):
			if path[i] == 0:
				continue
			for j in range(i, pow(size, 2)):
				if path[j] == 0:
					continue
				if path[i] > path[j]:
					bem += 1
		if (size % 2 != 0 and bem % 2 == 0) or (size % 2 == 0 and bem % 2 != 0):
			break
	return path


def parse_solve(node):
	solution = ""
	prev = node
	node = node.parent
	while node != None:
		diff = prev.getZero() - node.getZero()
		if diff == -1:
			solution += 'l'
		elif diff == 1:
			solution += 'r'
		elif diff < 0:
			solution += 't'
		else:
			solution += 'b'
		prev = node
		node = node.parent
	return solution[::-1]

@timeout(60.0)
def from_site(size, path, algo, heuristics):
	# path = [0, 10, 13, 15, 2, 3, 4, 8, 14, 7, 5, 6, 11, 1, 9, 12] - 48
	# path = [0, 6, 14, 3, 9, 5, 13, 7, 12, 2, 1, 8, 11, 10, 15, 4] - 46
	print(size)
	f = Algorithms(algo, size, heuristics)
	rez = f.solve(path)
	solution = parse_solve(rez['solution'])
	to_c = ""
	for el in path:
		to_c += "," + str(el)
	to_c = to_c[1:]

	# print("to c = ", to_c)
	c_module = CDLL('./adder.so')
	to_c = c_char_p(to_c.encode('utf-8'))
	algo_c = c_char_p(algo.encode('utf-8'))
	heuristics_c = c_char_p(heuristics.encode('utf-8'))
	c_module.python.restype = c_float
	c_time2 = c_module.python(size, to_c, algo_c, heuristics_c)
	# print("C TIME = ", c_time)
	# print("C TIME2 = ", c_time2)
	# call(["./a.out", str(size), to_c])
	# print("TIME = ", rez['time'])
	return {'c_time': c_time2 / 1000.0, 'python_time': rez['time'], 'solution': solution}
	# return {'time': rez['time']}


if __name__ == "__main__":
	size = 4
	path = getRandomPath(size)
	# print(path)
	path = [0, 10, 13, 15, 2, 3, 4, 8, 14, 7, 5, 6, 11, 1, 9, 12]
	# path = [6, 5, 1, 7, 0, 3, 4, 2, 8]
	# print(path)
	# final
	# f = Algorithms("idaStar", size, "patternDatabase")
	f = Algorithms("idaStar", size, "manhattan+linear2")
	rez = f.solve(path)
	print("TIME FINAL = ", rez['time'])
	# first
	# rez2 = from_site(size, path, False)
	# print("TIME FIRST = ", rez2)

# 4
# 0 10 13 15
# 2 3 4 8
# 14 7 5 6
# 11 1 9 12

# 413141161210921538715

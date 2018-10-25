from ctypes import *
from random import randint

from .Algorithms import *
from .Node import *
from .Heuristics import *


import multiprocessing.pool
import functools


def timeout(max_timeout):
	def timeout_decorator(item):
		@functools.wraps(item)
		def func_wrapper(*args, **kwargs):
			pool = multiprocessing.pool.ThreadPool(processes=1)
			async_result = pool.apply_async(item, args, kwargs)
			return async_result.get(max_timeout)
		return func_wrapper
	return timeout_decorator


def doRand(size):
	# goal = [i + 1 for i in range(pow(size, 2))]
	# goal[pow(size, 2) - 1] = 0
	bem = get_snake(size)
	# what_to_move = goal[bem.index(0)]
	# print(what_to_move)
	heuristics = Heuristics(['manhattan'], size, 0, 0)
	goal = Node(bem, size)
	for _ in range(500):
		child = goal.getChildrens(heuristics)
		i = randint(0, len(child) - 1)
		goal = child[i]
	return goal.field


def getRandomPath(size):
	return doRand(size)
	# path = []
	# while True:
	# 	path = doRand(size)
	# 	bem = 0
	# 	for i in range(pow(size, 2)):
	# 		if path[i] == 0:
	# 			continue
	# 		for j in range(i, pow(size, 2)):
	# 			if path[j] == 0:
	# 				continue
	# 			if path[i] > path[j]:
	# 				bem += 1
	# 	if (size % 2 != 0 and bem % 2 == 0) or (size % 2 == 0 and bem % 2 != 0):
	# 		break
	# return path


def parse_solve(node, heu):
	solution = ""
	prev = node
	node = node.parent
	while node != None:
		diff = heu.getZero(prev.field) - heu.getZero(node.field)
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
	f = Algorithms(algo, size, heuristics)
	rez = f.solve(path)
	solution = parse_solve(rez['solution'], f.heuristics)
	to_c = ""
	print(solution)
	for el in path:
		to_c += "," + str(el)
	to_c = to_c[1:]

	# TODO дописать snake на c
	c_time2 = -1

	# c_module = CDLL('./c/hello.so')
	# c_module = CDLL('./c/test.so')
	# to_c = c_char_p(to_c.encode('utf-8'))
	# algo_c = c_char_p(algo.encode('utf-8'))
	# heuristics_c = c_char_p(heuristics.encode('utf-8'))
	# c_module.python.restype = c_float
	# if algo != "bfs":
	# 	c_time2 = round(c_module.python(size, to_c, algo_c, heuristics_c) / 1000.0, 7)
	# else:
	# 	c_time2 = "Not available"

	return {'c_time': c_time2, 'python_time': round(rez['time'], 7), 'solution': solution, 'time_c': rez['time_c'], 'size_c': rez['size_c']}

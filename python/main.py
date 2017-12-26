from subprocess import call

from .Algorithms import *
from .generator import *

def getRandomPath(size):
	path = []
	while True:
		path = make_puzzle(size, False, 10000)
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


def from_site(size, path):
	# path = [0, 10, 13, 15, 2, 3, 4, 8, 14, 7, 5, 6, 11, 1, 9, 12]
	print(size)
	f = Algorithms("idaStar", size, "manhattan+linear2")
	rez = f.solve(path)
	to_c = ""
	for el in path:
		to_c += "," + str(el)
	to_c = to_c[1:]
	call(["./a.out", str(size), to_c])
	print("TIME = ", rez['time'])
	return rez['time']

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

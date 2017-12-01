from Node import *
from Algorithms import *
from generator import *
from solver import *

if __name__ == "__main__":
	path = []
	size = 4
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

	path = [0,10,13,15,2,3,4,8,14,7,5,6,11,1,9,12]
	print(path)
	# final
	f = Algorithms("idaStar", size, "manhattan+linear2")
	rez = f.solve(Node(path, size))
	print("TIME FINAL = ", rez['time'])
	# first
	rez2 = from_site(size, path, False)
	print("TIME FIRST = ", rez2)


# 4
# 0 10 13 15
# 2 3 4 8
# 14 7 5 6
# 11 1 9 12

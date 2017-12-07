import collections

import Node

size = 4
database_6_6_3 = {'file': "database_6_6_3", 'db': [[1,2,3,5,6,9,10],[4,7,8,11,12],[13,14,15]]}
database_5_5_5 = {'file': "database_5_5_5", 'db': [[1,2,3,5,6,9],[4,7,8,11,12],[10,13,14,15]]}
database_7_8 = {'file': "database_7-8", 'db': [[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15]]}

def check_not_in(node, arr):
	for el in arr:
		if el.field == node.field:
			return False
	return True

def bfs(initial):
	visited, queque = set(), collections.deque([root])
	while queque:
		vertex = queque.popleft()
		for neighbor in current.getChildrens():
			if check_not_in(neighbor, visited):
				visited.add(neighbor)
				child.setParent(current)
				queque.append(neighbor)


def generate(database):
	pass
	# for db in database:
		# file_size = 

if __name__ == '__main__':
	i = 255

	# Create one byte from the integer 16
	single_byte = i.to_bytes(1, byteorder='big', signed=False) 
	print(single_byte)

	for i in range(6):
		print(i << 2)
	print(15 << 20)

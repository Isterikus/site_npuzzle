from json import load
from math import sqrt

class Heuristics():
	def __init__(self, heuristics, size, what_to_move, to_remember):
		self.heuristics = heuristics
		self.size = size
		self.all_cells = pow(size, 2)
		self.real_positions = [{} for i in range(self.all_cells)]
		self.realPositions()
		# self.patterns = [[1, 2, 3, 5, 6], [4, 7, 8, 11, 12], [9, 10, 13, 14, 15]]  # 5-5-5 2
		self.patterns = [[1, 2, 3, 5, 6], [4, 7, 8, 11, 12], [9, 13, 14, 15, 0]]
		self.databases = []
		self.what_to_move = what_to_move
		self.to_remember = to_remember
		print(what_to_move, to_remember)
		for i in range(len(self.patterns)):
			file = "DATABASE_5_5_5-" + str(i + 1)
			with open("./databases/" + file, 'r') as f:
				self.databases.append(load(f))

	def getZero(self, field):
		for i in range(len(field)):
			if field[i] == self.what_to_move:
				return i

	def realPositions(self):
		for c in range(1, self.all_cells):
			self.real_positions[c]['i'] = (c - 1) // self.size
			self.real_positions[c]['j'] = (c - 1) % self.size

	def manhattan(self, field):
		h = 0
		for pos in range(self.all_cells):
			if field[pos] != 0:
				h += (abs(pos // self.size - self.real_positions[field[pos]]['i'])
					+ abs(pos % self.size - self.real_positions[field[pos]]['j']))
		return h

	def linear(self, field):
		h = 0
		for i in range(self.size):
			max_i = -1
			max_j = -1
			for j in range(self.size):
				val_i = field[i * self.size + j]
				val_j = field[j * self.size + i]
				if val_i != 0 and (val_i - 1) // self.size == i:
					if val_i > max_i:
						max_i = val_i
					else:
						h += 2
				if val_j != 0 and val_j % self.size == i + 1:
					if val_j > max_j:
						max_j = val_j
					else:
						h += 2
		return h

	def linear2(self, field):
		h = 0
		for i in range(self.size):
			for j in range(self.size):
				pos = i * self.size + j
				for l in range(i, self.size):
					if field[pos] > field[l * self.size + j]:
						h += 2
				for k in range(j, self.size):
					if field[pos] > field[i * self.size + k]:
						h += 2
		return h

	def patternDatabase(self, node):
		ret = 0
		for i in range(len(self.patterns)):
			ret += self.databases[i][node.code(self.patterns[i], self.what_to_move, self.to_remember)]
		return ret

	def tilesOut(self, field):
		h = 0
		for pos in range(self.all_cells):
			if field[pos] != 0:
				h += 1 if (pos // self.size - self.real_positions[field[pos]]['i']) else 0
				h += 1 if (pos % self.size - self.real_positions[field[pos]]['j']) else 0
		return h

	def misplacedTiles(self, field):
		h = 0
		i = 0
		for val in field:
			if val == 0:
				if i != len(field) - 1:
					h += 1
			elif i // self.size != self.real_positions[val]['i'] or i % self.size != self.real_positions[val]['j']:
				h += 1
			i += 1
		return h

	def euclideanDistance(self, field):
		h = 0.0
		for pos in range(self.all_cells):
			if field[pos] != 0:
				h += sqrt(pow(pos // self.size - self.real_positions[field[pos]]['i'], 2)
					+ pow(pos % self.size - self.real_positions[field[pos]]['j'], 2))
		return h

	def getH(self, node):
		h = 0
		for heuristic in self.heuristics.split('+'):
			if heuristic == "manhattan":
				h += self.manhattan(node.field)
			elif heuristic == "linear":
				h += self.linear(node.field)
			elif heuristic == "linear2":
				h += self.linear2(node.field)
			elif heuristic == "patternDatabase":
				h += self.patternDatabase(node)
			elif heuristic == "tilesOut":
				h += self.tilesOut(node.field)
			elif heuristic == "misplacedTiles":
				h += self.misplacedTiles(node.field)
			elif heuristic == "euclideanDistance":
				h += self.euclideanDistance(node.field)
		return h

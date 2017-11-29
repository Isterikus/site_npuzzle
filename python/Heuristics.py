class Heuristics():
	def __init__(self, heuristics, size):
		self.heuristics = heuristics
		self.size = size
		self.real_positions = [{} for i in range(pow(self.size, 2))]
		self.realPositions()

	def realPositions(self):
		for c in range(1, pow(self.size, 2)):
			self.real_positions[c]['i'] = (c - 1) // self.size
			self.real_positions[c]['j'] = (c - 1) % self.size

	def manhattan(self, field):
		h = 0
		for i in range(self.size):
			for j in range(self.size):
				if field[i][j] != 0:
					h += abs(self.real_positions[field[i][j]]['i'] - i) + abs(self.real_positions[field[i][j]]['j'] - j)
		return h

	def linear(self, field):
		h = 0
		for i in range(self.size):
			max_i = -1
			max_j = -1
			for j in range(self.size):
				val_i = field[i][j]
				val_j = field[j][i]
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

	def getH(self, field):
		h = 0
		for heuristic in self.heuristics.split('+'):
			if heuristic == "manhattan":
				h += self.manhattan(field)
			elif heuristic == "linear":
				h += self.linear(field)
		return h

# field = [[3,7,2],[0,1,5],[6,4,8]]
# field = [[7,6,2],[5,0,1],[4,8,3]]
# field = [[4,2,5],[1,0,6],[3,8,7]]
# heu = Heuristics("manhattan+linear", 3)
# h = heu.getH(field)
# print(h)

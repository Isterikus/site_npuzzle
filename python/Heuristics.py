class Heuristics():
	def __init__(self, heuristics, size):
		self.heuristics = heuristics
		self.size = size
		self.all_cells = pow(size, 2)
		self.real_positions = [{} for i in range(self.all_cells)]
		self.realPositions()

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

	def patternDatabase(self, field):
		base = [[2,3,4],[1,5,6,9,10,13],[7,8,11,12,14,15]]
		h = [0,0,0]
		for pos in range(self.all_cells):
			if field[pos] != 0:
				for i in range(3):
					if field[pos] in base[i]:
						h[i] += (abs(pos // self.size - self.real_positions[field[pos]]['i'])
							+ abs(pos % self.size - self.real_positions[field[pos]]['j']))
		return max(h)

	def test(self, arr, val):
		i = 0
		while i < len(arr):
			if arr[i] == val:
				return i
			i += 1

	def patternDatabase2(self, field):
		base = [[],[],[]]
				# [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]
		base[0] = [-1, 2, 3, 4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
		base[1] = [ 1,-1,-1,-1, 5, 6,-1,-1, 9,10,-1,-1,13,-1,-1]
		base[2] = [-1,-1,-1,-1,-1,-1, 7, 8,-1,-1,11,12,-1,14,15]
		# base = [[2,3,4],[1,5,6,9,10,13],[7,8,11,12,14,15]]
		h = [0,0,0]
		for pos in range(self.all_cells):
			for i in range(3):
				if field[pos] in base[i]:
					h[i] |= pos << (4 * field[pos])
		print(h)
		return max(h)

	def getH(self, field):
		h = 0
		for heuristic in self.heuristics.split('+'):
			if heuristic == "manhattan":
				h += self.manhattan(field)
			elif heuristic == "linear":
				h += self.linear(field)
			elif heuristic == "linear2":
				h += self.linear2(field)
			elif heuristic == "patternDatabase":
				h += self.patternDatabase(field)
			elif heuristic == "patternDatabase2":
				h += self.patternDatabase2(field)
		return h

# field = [0,10,13,15,2,3,4,8,14,7,5,6,11,1,9,12]
# # field = [3,7,2,0,1,5,6,4,8]
# # field = [7,6,2,5,0,1,4,8,3]
# # field = [4,2,5,1,0,6,3,8,7]
# heu = Heuristics("patternDatabase2", 4)
# h = heu.getH(field)
# print(h)
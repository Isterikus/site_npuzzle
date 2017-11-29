class Heuristics():
	def __init__(self, heuristics):
		self.heuristics = heuristics

	def manhattan(self, field):
		h = 0
		

	def getH(self, field):
		h = 0
		for heuristic in self.heuristic.split('+'):
			if heuristic == "manhattan":
				h += self.manhattan(field)
		
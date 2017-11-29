import copy

class Node():
	def __init__(self, field, size):
		self.field = field
		self.size = size
		self.parent = None
		self.g = 0

	def getZero(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.field[i][j] == 0:
					return [i, j]
	
	def getField(self):
		return self.field

	def setParent(self, parent):
		self.parent = parent
		self.g = parent.getG() + 1

	def setG(self, g):
		self.g = g

	def getG(self):
		return self.g

	def getChildrens(self):
		i,j = self.getZero()
		childrens = []

		if i > 0:
			tmp_field = copy.copy(self.field)
			tmp_field[i][j],tmp_field[i-1][j] = tmp_field[i-1][j],tmp_field[i][j]
			childrens.append(Node(tmp_field, size))
		if i < self.size - 1:
			tmp_field = copy.copy(self.field)
			tmp_field[i][j],tmp_field[i+1][j] = tmp_field[i+1][j],tmp_field[i][j]
			childrens.append(Node(tmp_field, size))
		if j > 0:
			tmp_field = copy.copy(self.field)
			tmp_field[i][j],tmp_field[i][j-1] = tmp_field[i][j-1],tmp_field[i][j]
			childrens.append(Node(tmp_field, size))
		if j < self.size - 1:
			tmp_field = copy.copy(self.field)
			tmp_field[i][j],tmp_field[i][j+1] = tmp_field[i][j+1],tmp_field[i][j]
			childrens.append(Node(tmp_field, size))
		return childrens

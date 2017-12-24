from copy import copy


class Node:
	def __init__(self, field, size):
		self.field = field
		self.size = size
		self.all_cells = pow(self.size, 2)
		self.parent = None
		self.g = 0

	def getZero(self):
		for i in range(self.all_cells):
			if self.field[i] == 0:
				return i

	def getField(self):
		return self.field

	def setParent(self, parent):
		self.parent = parent
		# self.g = parent.getG() + 1

	def getParent(self):
		return self.parent

	def setG(self, g):
		self.g = g

	def getG(self):
		return self.g

	def find(self, val):
		for i in range(self.size):
			for j in range(self.size):
				if self.field[i * self.size + j] == val:
					return {'i': i, 'j': j}

	def code(self, pattern):
		code = ""
		for val in pattern:
			pos = self.find(val)
			code += str(pos['i']) + str(pos['j'])
		return code

	def getChildrens(self):
		pos = self.getZero()
		childrens = []
		if pos >= self.size:
			tmp_field = copy(self.field)
			tmp_field[pos], tmp_field[pos-self.size] = tmp_field[pos-self.size], 0
			childrens.append(Node(tmp_field, self.size))
		if pos < self.all_cells - self.size:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos+self.size] = tmp_field[pos+self.size],0
			childrens.append(Node(tmp_field, self.size))
		if pos % self.size != 0:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos-1] = tmp_field[pos-1],0
			childrens.append(Node(tmp_field, self.size))
		if (pos + 1) % self.size != 0:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos+1] = tmp_field[pos+1],0
			childrens.append(Node(tmp_field, self.size))
		i = 0
		while i < len(childrens):
			if self.getParent() is not None and self.getParent().field == childrens[i].field:
				del childrens[i]
			i += 1
		return childrens

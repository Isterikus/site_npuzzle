from copy import copy


class Node:
	def __init__(self, field, size, action='0'):
		self.field = field
		self.size = size
		# self.all_cells = pow(self.size, 2)
		self.parent = None
		self.h = 0
		self.g = 0
		self.action = action

	def getZero(self):
		i = 0
		for val in self.field:
			if val == 0:
				return i
			i += 1

	def getField(self):
		return self.field

	def setParent(self, parent):
		self.parent = parent
		# self.g = parent.getG() + 1

	def getParent(self):
		return self.parent

	def getG(self):
		return self.g

	def setG(self, g):
		self.g = g

	def setH(self, h):
		self.h = h

	def getH(self):
		return self.h

	def find(self, val):
		for i in range(self.size):
			for j in range(self.size):
				if self.field[i * self.size + j] == val:
					return {'i': i, 'j': j}

	def code(self, pattern):
		code = ""
		for val in self.field:
			if val not in pattern:
				code += "0"
			elif val == 0:
				code += "0"
			else:
				code += str(val)
		return code

	def getChildrens(self):
		pos = self.getZero()
		childrens = []
		if self.action != 'b' and pos >= self.size:
			tmp_field = copy(self.field)
			tmp_field[pos], tmp_field[pos-self.size] = tmp_field[pos-self.size], 0
			childrens.append(Node(tmp_field, self.size, 't'))
		if self.action != 't' and pos < len(self.field) - self.size:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos+self.size] = tmp_field[pos+self.size],0
			childrens.append(Node(tmp_field, self.size, 'b'))
		if self.action != 'r' and pos % self.size != 0:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos-1] = tmp_field[pos-1],0
			childrens.append(Node(tmp_field, self.size, 'l'))
		if self.action != 'l' and (pos + 1) % self.size != 0:
			tmp_field = copy(self.field)
			tmp_field[pos],tmp_field[pos+1] = tmp_field[pos+1],0
			childrens.append(Node(tmp_field, self.size, 'r'))
		return childrens

class Node:
	def __init__(self, data=None):
		self.data = data
		self.prior = None
		self.left = None
		self.right = None
		self.equal = None

class TST:
	def __init__(self):
		self.root = None

	def _insert(self, current, word, index, prior):
		char = word[index]
		if current == None:
			current = Node(char)
		if char < current.data:
			current.left = self._insert(current.left, word, index, prior)
		elif char > current.data:
			current.right = self._insert(current.right, word, index, prior)
		else:
			if index == len(word)-1:
				current.prior = prior
			else:
				current.equal = self._insert(current.equal, word, index+1, prior)
		return current

	def insert(self, word, prior):
		self.root = self._insert(self.root, word, 0, prior)

	def _search(self, current, word, index):
		char = word[index]
		if current == None:
			return None
		if char < current.data:
			return self._search(current.left, word, index)
		elif char > current.data:
			return self._search(current.right, word, index)
		else:
			if index == len(word)-1:
				return current.prior
			return self._search(current.equal, word, index+1)

	def search(self, word):
		return self._search(self.root, word, 0)

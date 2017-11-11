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

	def _insert(self, current, word, length, index, prior):
		char = word[index]
		if current == None:
			current = Node(char)
		if char < current.data:
			current.left = self._insert(current.left, word, length, index, prior)
		elif char > current.data:
			current.right = self._insert(current.right, word, length, index, prior)
		else:
			if index == length-1:
				current.prior = prior
			else:
				current.equal = self._insert(current.equal, word, length, index+1, prior)
		return current

	def insert(self, word, prior = 1):
		self.root = self._insert(self.root, word, len(word), 0, prior)

	def _search(self, current, word, length, index):
		char = word[index]
		if current == None:
			return None
		if char < current.data:
			return self._search(current.left, word, length, index)
		elif char > current.data:
			return self._search(current.right, word, length, index)
		else:
			if index == length-1:
				return current.prior
			return self._search(current.equal, word, length, index+1)

	def search(self, word):
		return self._search(self.root, word, len(word), 0)
		
	def _depth(self, current, count):
		if current == None:
			return count
		return max(self._depth(current.left, count+1), self._depth(current.right, count+1), self._depth(current.equal, count+1))
	def depth(self):
		return self._depth(self.root, 0)
		

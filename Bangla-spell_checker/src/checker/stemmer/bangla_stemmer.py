import re, os

class RuleFileParser(object):
	
	CURLY_OPEN = "{"
	CURLY_CLOSE = "}"
	
	def __init__(self, rule_file_path = "common.rules"):
		current_abs_path = os.path.dirname(os.path.abspath(__file__))
		rule_file_path = current_abs_path+'/'+rule_file_path
		self.lines = []
		self.passes = []
		self.replaceRule = {}
		self.dependant_vowels_unicode = re.compile(r'[\u09BE-\u09C4\u09C7-\u09C8\u09CB-\u09CD]', re.UNICODE)

		with open(rule_file_path, 'r', encoding = "utf-8") as infile:
			for line in infile:
				line = self.commentTrim(line)
				line = line.strip()
				if len(line) == 0:
					continue
				line, replace = self.extractReplaceRule(line)
				self.replaceRule[line] = replace
				self.lines.append(line)

			l, cnt = len(self.lines), 0
			for i in range(l):
				if self.lines[i] == self.CURLY_OPEN:
					self.passes.append([])
					i += 1
					while i<l and self.lines[i]!=self.CURLY_CLOSE:
						self.passes[cnt].append(self.lines[i])
						i += 1
					cnt += 1


	def extractReplaceRule(self, string):
		if "->" in string:
			split = string.split("->")
			return split[0].strip(), split[1].strip()
		return string, ""

	def commentTrim(self, string):
		return re.sub("#.*", "", string)

	def check(self, word):
		l = len(re.sub(self.dependant_vowels_unicode, "", word))
		l -= word.count("\u09CD")
		return l >=2

	def stemOfWord(self, word):
		for _pass in self.passes:
			for replace_prefix in _pass:
				pattern = re.compile(".*"+replace_prefix+"$")
				if pattern.match(word):
					replace_suffix = self.replaceRule[replace_prefix]
					new_word = word[:(len(word) - len(replace_prefix))]
					if len(replace_suffix):
						rest_word = word[(len(word) - len(replace_prefix)):]
						for i in range(len(replace_suffix)):
							if replace_suffix[i] == ".":
								new_word += rest_word[i]
							else:
								new_word += replace_suffix[i]
						word = new_word
					elif self.check(new_word):
						word = new_word
					break

		return word

	def stemOfWords(self, words):
		words = [self.stemOfWord(w) for w in words]
		return words


bangla_stemmer = RuleFileParser()


if __name__ == '__main__':
	print("hi")
	rule_file_parser = RuleFileParser()
	with open("input.txt", "r") as lines:
		with open("output.txt", "w") as file:
			for line in lines:
				stem_word = rule_file_parser.stemOfWord(line.strip())
				print(stem_word)
				file.write(stem_word+"\n")

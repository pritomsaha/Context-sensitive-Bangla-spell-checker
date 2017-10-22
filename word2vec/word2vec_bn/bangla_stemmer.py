
class RuleFileParser(object):
	
	CURLY_OPEN = "{"
	CURLY_CLOSE = "}"
	
	def __init__(self, rule_file_path):
		self.lines = []
		self._pass = []
		self.st = set()
		self.replaceRule = {}
		dependantCharSetInstallation()

		with open('rule_file_path', 'r', encoding = "utf-8") as infile:
			for line in infile:
				line = line.strip()
				if len(line) == 0:
					continue

	def extractReplaceRule(string):
		if "->" in string:



	def dependantCharSetInstallation():
		st.add('া')
		st.add('ি')
		st.add('ী')
		st.add('ে')
		st.add('ু')
		st.add('ূ')
		st.add('ো')


		

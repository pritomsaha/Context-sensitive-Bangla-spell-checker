import re, os

bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

word_freq = {}

def  get_wordlist(text):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split(" ")
	return (words)


def count_word(folder_name):
	for file_name in os.listdir(folder_name):
		with open(folder_name+'/'+file_name, 'r', encoding = "utf-8") as infile:
			for line in infile:
				words = get_wordlist(line)
				for word in words:
					count = word_freq.get(word, 0)
					word_freq[word] = count + 1


def create_word_freq():
	folders = ['newspaper', 'web', 'wiki']
	for folder in folders:
		count_word(folder)

	file = open ("words_freq.txt", "w", encoding = "utf-8")	

	with open('bn_lexicon.txt', 'r', encoding = "utf-8") as infile:
		for line in infile:
			word = line.strip()
			count = word_freq.get(word, 1)
			file.write(word+" "+str(count)+"\n")

	file.close()

def add_test_word():
	words = []
	with open('bn_lexicon.txt', 'r', encoding = 'utf-8') as infile:
		for line in infile:
			words.append(line.strip())

	with open('test.txt', 'r', encoding = 'utf-8') as infile:
		for line in infile:
			word = line.split("-")[1].strip()
			if word not in words:
				words.append(word)

	words = sorted(words)

	with open('bn_lexicon.txt', 'w', encoding = 'utf-8') as infile:
		for word in words:
			infile.write(word+"\n")


def create_encoded_freq_lexicon():
	encodes = {"অ" :"o",  "আ": "a", "া": "a",  "ই": "i", "ঈ": "i", "ি":"i", "ী" : "i", "উ" : "u", "ঊ": "u", "ু": "u", "ূ": "u", "এ": "e", "ে": "e", "ঐ": "oi", "ৈ": "oi", "ও": "o", "ঔ": "ou","ৌ": "ou", "ক": "k", "খ": "k", "গ": "g", "ঘ": "g", "ঙ": "ng", "ং": "ng", "চ": "c", "ছ": "c", "য": "j", "জ": "j", "ঝ": "j", "ঞ": "n", "ট": "T", "ঠ": "T", "ড": "D", "ঢ": "D", "ঋ": "ri", "র": "r", "ড়": "r", "ঢ়": "r", "ন": "n", "ণ": "n", "ত": "t", "থ": "t", "দ": "d", "ধ": "d", "প": "p", "ফ": "p", "ব": "b", "ভ": "b", "ম": "m", "য়": "y", "ল": "l", "শ": "s", "স": "s", "ষ": "s", "হ": "h", "ঃ" : "h", "ৎ": "t"}
	
	def get_encoded_word(word):
		encoded_word = ""
		for w in word:
			if w in encodes:
				encoded_word += encodes[w]
		return encoded_word

	with open('words_freq.txt', 'r', encoding = "utf-8") as infile:
		file = open('bn_lex_enc_freq.txt', 'w', encoding = "utf-8")
		for line in infile.readlines():
			# print(line)
			word, count = line.strip().split()
			encoded_word = get_encoded_word(word)
			file.write(encoded_word+" "+word+" "+count+"\n")
			
		file.close()


if __name__ == '__main__':
	add_test_word()
	create_word_freq()
	create_encoded_freq_lexicon()

	


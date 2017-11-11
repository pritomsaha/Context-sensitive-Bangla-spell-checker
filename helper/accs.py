import re, os
from phonetic_encoder import soundex_encode, doublemetaphone_encode
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

word_freq = {}
bnwordlist_path = "bnwordlist.txt"
bnwordfreq_path = "bnwordfreq.txt"
encwordlist_path = "encwordlist.txt"
corpus_path = "../corp"

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
	count_word(corpus_path)
	file = open (bnwordfreq_path, "w", encoding = "utf-8")	

	with open(bnwordlist_path, 'r', encoding = "utf-8") as infile:
		for line in infile:
			word = line.strip()
			count = word_freq.get(word, 1)
			file.write(word+" "+str(count)+"\n")

	file.close()

def add_test_word():
	words = set()
	with open(bnwordlist_path, 'r', encoding = 'utf-8') as infile:
		for line in infile:
			words.add(line.strip())

	with open('test.txt', 'r', encoding = 'utf-8') as infile:
		for line in infile:
			word = line.split("-")[1].strip()
			words.add(word)

	words = sorted(list(words))

	with open(bnwordlist_path, 'w', encoding = 'utf-8') as infile:
		for word in words:
			infile.write(word+"\n")


def create_encoded_freq_lexicon():
	
	def get_encoded_word(word):
		return doublemetaphone_encode(word)

	with open(bnwordfreq_path, 'r', encoding = "utf-8") as infile:
		file = open(encwordlist_path, 'w', encoding = "utf-8")
		for line in infile.readlines():
			word, count = line.strip().split()
			encoded_word = get_encoded_word(word)
			file.write(encoded_word+" "+word+" "+count+"\n")
			
		file.close()


if __name__ == '__main__':
#	add_test_word()
#	create_word_freq()
	create_encoded_freq_lexicon()

	


import re, os
from phonetic_encoder import soundex_encode, doublemetaphone_encode
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

word_freq = {}
bnwordlist_path = "bnwordlist.txt"
bnwordfreq_path = "bnwordfreq.txt"
encwordlist_path = "../sd_encwordlist.txt"
corpus_path = "../corp"
doublemetaphone = True
if doublemetaphone:
	encwordlist_path = "dm_encwordlist.txt"

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


def get_word_freq():
	count_word(corpus_path)
	with open(bnwordlist_path, 'r', encoding = "utf-8") as infile:
		for line in infile:
			word = line.strip()
			count = word_freq.get(word, 1)
			yield word, count
			
# def add_test_word():
# 	words = set()
# 	with open(bnwordlist_path, 'r', encoding = 'utf-8') as infile:
# 		for line in infile:
# 			words.add(line.strip())

# 	with open('test.txt', 'r', encoding = 'utf-8') as infile:
# 		for line in infile:
# 			word = line.split("-")[1].strip()
# 			words.add(word)

# 	words = sorted(list(words))

# 	with open(bnwordlist_path, 'w', encoding = 'utf-8') as infile:
# 		for word in words:
# 			infile.write(word+"\n")

def create_encoded_freq_lexicon():
	
	def get_encoded_word(word):
		return doublemetaphone_encode(word) if doublemetaphone else soundex_encode(word)

	with open(encwordlist_path, "w", encoding = "utf-8") as file:
		dic_word_freq = get_word_freq()
		for word, count in dic_word_freq:
			encoded_word = get_encoded_word(word)
			file.write(encoded_word+" "+word+" "+str(count)+"\n")

def chunks(data, rows = 10000):
	l = len(data)
	for i in range(0, l, rows):
		yield data[i:i+rows]

def save_dic_to_db():
	import sqlite3
	conn = sqlite3.connect("../Spell-Checker/spell_checker.db")
	cur = conn.cursor()
	cur.execute("create table if not exists dictionary (word varchar(30) NOT NULL, encoded_word varchar(30) NOT NULL);")
	counter = 1
	sql_create_row = "insert into dictionary (word, encoded_word) values(?, ?);"
	with open('../dm_encwordlist.txt', 'r') as file:
		data = file.readlines()
		chunks_data = chunks(data)
		for chunk in chunks_data:
			rows = []
			for line in chunk:
				data = line.strip().split()
				if len(data) == 3:
					rows.append((data[1], data[0]))
				
			cur.executemany(sql_create_row, rows)
			print(counter)
			counter += 1

	conn.commit()
	conn.close()

if __name__ == '__main__':
	 create_encoded_freq_lexicon()
#	save_dic_to_db()

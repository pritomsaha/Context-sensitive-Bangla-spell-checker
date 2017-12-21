import re, os
from phonetic_encoder import soundex_encode, doublemetaphone_encode
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]+', re.UNICODE)
bn_al_pattern = re.compile(r'[\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]+', re.UNICODE)


word_freq = {}
bnwordlist_path = "bnwordlist2.txt"
bnwordfreq_path = "bnwordfreq.txt"
encwordlist_path = "sd_encwordlist.txt"
corpus_path = "../corpus/initial_corp"
doublemetaphone = False
if doublemetaphone:
	encwordlist_path = "dm_encwordlist.txt"

def get_wordlist(text):
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
	word_count = {}
	with open(bnwordlist_path, 'r', encoding = "utf-8") as infile:
		for line in infile:
			word = line.strip()
			count = word_freq.get(word, 1)
			word_count[word] = count
#			yield word, count
	return word_count
			
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
		max_count = max(dic_word_freq.values())
		print(max_count)
		for word in dic_word_freq:
			count = dic_word_freq[word]/max_count
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
	
#def sample(text):
#	words = []
#	separators = []
#	word = ""
#	
#	words = re.split(bn_char_pattern,  text)
#	separators = re.split(bn_al_pattern, text)
#	separators = list(filter(None, separators))
#	i = 0
#	new_txt = []
#	for w in words:
#		new_txt.append(w)
#		if i < len(separators):saq78
#			new_txt.append(separators[i])
#			i += 1
#		
#	print(words,"\n", separators)
#	print(new_txt)


def clean_list():
	f = open("bangla_words2.txt", "w", encoding ="utf-8")
	with open("bangla_words.txt", "r") as infile:
		for line in infile:
			words = line.strip().split()
			l = ""
			for w in words:
				if "০" not in w:
					print(w)
					l += w+" "
			f.write(l.strip()+"\n")
			
	f.close()
		
	
def create_sentences():
	with open("others_.txt", "r") as lines:
		with open("others.txt", "a") as file:
			for line in lines:
				sentences = re.split(r"\।|\?", line)
				sentences = "\n".join(sentence.strip() for sentence in sentences[:-1])				
				file.write(sentences)
			
if __name__ == '__main__':
#	clean_list()
#	sample("বাংলাদেশ,,, ভাল,, সধদ  সদকজফ সদকজফ   সদকজফফ স্কদজফ   সদকজফফ")
	create_encoded_freq_lexicon()
#	create_sentences()
#	save_dic_to_db()



উইকিপিডিয়াইয় একটি অন্তস্থ সার্চ ইঞ্জিন আছে যেটা উইকিপিডিয়ায় তথ্য খুজে পেতে সাহায্য করে। অনুসন্ধান বক্সটি সাধারন উইকিপিডিয়া পাতার উপরে বাম পাশে থাকে অথবা অন্য ধরনের পাতায় এটি হাতের বাম পাশে টুলবক্সে থাকে। এই অনুসন্ধান বক্সটি আপনি যা খুজতে চাচ্ছেন সেই পাতায় নিয়ে যাবে, অন্যথায় এটি অনুসন্ধান ফলাফল প্রকাশ করবে। পূর্ন অনুসন্ধান ফলাফল পেতে ড্রপ ডাউন তালিকার সর্বশেষ অংশে ক্লিক করুন অথবা একটি ফাকা অনুসন্ধান করুন।


মূল অনুসন্ধান বক্সটি নিবন্ধের শ্রেণী অনুসন্ধান করে না। আপনি একটি নাল অনুসন্ধানের (অনুসন্ধান বাক্স ফাকা থাকে, আতশি কাচের ছবিতে বা অনুসন্ধান বোতাম চাপতে হয়) মাধ্যমে আধুনিক অনুসন্ধান প্রদর্শন করাতে পারেন। আধুনিক অনুসন্ধানে তথ্যের শ্রেণী সহ অনুসন্ধান করতে চাইলে উচ্চতর আধুনিক অনুসন্ধান সহ অন্যান্য বাটনে ক্লিক করতে পারেন।

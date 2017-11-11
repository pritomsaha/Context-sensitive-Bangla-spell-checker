import re, os
import time
from collections import Counter
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
corpus_path = "../corp"
stopwords_path = "../stop-words.txt"
stopwords = []

def  get_bn_wordlist(text, remove_stopwords = False):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [w for w in words if w not in stopwords]

	return (words)

class Sentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for file_name in os.listdir(self.dirname):
			with open(os.path.join(self.dirname, file_name), 'r', encoding = "utf-8") as infile:
				for line in infile:
					wordlist = get_bn_wordlist(line, True)
					yield wordlist

def generate_ngram_count(n):
	ngrams = []
	sentences = Sentences(corpus_path)
	for sentence in sentences:
		l = len(sentence)
		for i in range(0, l-n+1):
			tupple = ()
			for k in range(n):
				tupple += (sentence[i+k],)
			ngrams.append(tupple)

	save_ngrams(Counter(ngrams), n)

def  save_ngrams(ngrams, n):
	with open(str(n)+"_gram.txt", "a") as file:
		for key in ngrams:
			ngram_str = "_".join(k for k in key)
			file.write(ngram_str+"	"+ str(ngrams[key])+"\n")
			

def build_TST():
	from TST import TST
	tst = TST()
	corpus_path = "n-gram_corpus"
	
	for file_name in os.listdir(corpus_path):
		with open(os.path.join(corpus_path, file_name), 'r', encoding = "utf-8") as file:
			data = file.readlines()
			chunks_data = chunks(data)
			counter = 1
			for chunk in chunks_data:
				for line in chunk:
					data = line.strip().split()
					if len(data) == 2:
						tst.insert(data[0], int(data[1]))
				print(counter)
				counter += 1
	
	print("success")
	inp = int(input("proceed to see depth?"))
	if inp:
		print(tst.depth())

def main():
	stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')
	generate_ngram_count(1)
	generate_ngram_count(2)
	generate_ngram_count(3)

def chunks(data, rows = 10000):
	l = len(data)
	for i in range(0, l, rows):
		yield data[i:i+rows]

def save_to_db():
	import sqlite3
	conn = sqlite3.connect("ngrams.db")
	cur = conn.cursor()
	start = time.time()
	# sql_create_table = "create table if not exists bigrams (grams varchar(50) NOT NULL unique,count integer NOT NULL);"
	# cur.execute(sql_create_table)
	counter = 1
	sql_create_row = "insert into bigrams (grams, count) values(?, ?);"
	with open('2_gram.txt', 'r') as file:
		data = file.readlines()
		chunks_data = chunks(data)
		for chunk in chunks_data:
			rows = []
			for line in chunk:
				data = line.strip().split()
				if len(data) == 2:
					rows.append((data[0], int(data[1])))
				
			cur.executemany(sql_create_row, rows)
			print(counter)
			counter += 1

	conn.commit()
	conn.close()
	print(time.time() - start)
	

if __name__ == '__main__':
	# main()
	build_TST()


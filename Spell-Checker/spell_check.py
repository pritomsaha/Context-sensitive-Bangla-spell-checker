import sqlite3
import re
conn = sqlite3.connect("ngrams.db")
cur = conn.cursor()


bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
stopwords_path = "../stop-words.txt"
stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')

def  get_bn_wordlist(text, remove_stopwords = False):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [w for w in words if w not in stopwords]

	return words

def get_ngram_count(text, n):
	table_name = "bigrams" if n==2 else "trigrams" 
	result = cur.execute("select count from "+table_name+" where grams ='"+text+"';").fetchone()
	if result:
		return result[0]
	else: return 0

def weighted_score(left_bigram, right_bigram, trigram):
	return left_bigram


def detect(sentence):
	words = get_bn_wordlist(sentence)
	l = len(words)

	for i in range(l):
		left_bigram, right_bigram, trigram = 0, 0, 0
		if i-1 > 0:
			left_bigram = get_ngram_count(words[i-1]+"_"+words[i], 2)
		if i+1 < l:
			right_bigram = get_ngram_count(words[i]+"_"+words[i+1], 2)
		if i-1 > 0 and i+1 < l:
			trigram = get_ngram_count(words[i-1]+"_"+words[i]+"_"+words[i+1], 3)

		print (left_bigram, right_bigram, trigram)




if __name__ == '__main__':

	detect("অন্য কেউ নেই")




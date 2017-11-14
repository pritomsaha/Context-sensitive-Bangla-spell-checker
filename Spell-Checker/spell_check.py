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

def get_ngram_count(text_grams):
	# table_name = "bigrams" if n==2 else "trigrams" 
	counts = [0, 0, 0]
	if text_grams[0]:
		result = cur.execute("select count from bigrams where grams ='"+text_grams[0]+"_"+text_grams[1]+"';").fetchone()
		if result:
			counts[0] = result[0]
	if text_grams[2]:
		result = cur.execute("select count from bigrams where grams ='"+text_grams[1]+"_"+text_grams[2]+"';").fetchone()
		if result:
			counts[1] = result[0]
	if not None in text_grams:
		result = cur.execute("select count from trigrams where grams ='"+text_grams[0]+"_"+text_grams[1]+"_"+text_grams[2]+"';").fetchone()
		if result:
			counts[2] = result[0]

	return counts

def weighted_score(left_bigram, right_bigram, trigram):
	return left_bigram


def detect(sentence):
	words = get_bn_wordlist(sentence)
	l = len(words)

	for i in range(l):
		left_bigram, right_bigram, trigram = 0, 0, 0
		confusion_set = []
		text_grams = [None, words[i], None]
		if i-1 > 0:
			text_grams[0] = words[i-1]
		if i+1 < l:
			text_grams[2] = words[i+1]
		
		if not sum(get_ngram_count(text_grams)):
			print(False)




if __name__ == '__main__':

	detect("অন্য কেউ নেই")




import sqlite3
import re, time
from suggestion_generation import get_suggestions
db_name = "spell_checker.db"
conn = sqlite3.connect(db_name)
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

def weighted_score(count, total):
	return 0.25*(count[0]/total[0]+count[1]/total[1]) + 0.5*count[2]/total[2]

def get_total(counts):
	values = list(counts.values())
	total = [0,0,0]
	for v in values:
		total[0] += v[0]
		total[1] += v[1]
		total[2] += v[2]
	for i in range(3):
		if total[i] == 0:
			 total[i] = 1
	return total

def detect(sentence):
	words = get_bn_wordlist(sentence)
	l = len(words)

	for i in range(l):
		counts = {}
		text_grams = [None, words[i], None]
		if i-1 > 0:
			text_grams[0] = words[i-1]
		if i+1 < l:
			text_grams[2] = words[i+1]
		
		counts[words[i]] = get_ngram_count(text_grams)
		confusion_set = get_suggestions(words[i])
		confusion_set[words[i]] = (0.0,)
		for word in confusion_set:
			text_grams[1] = word
			counts[word] = get_ngram_count(text_grams)
		
		total = get_total(counts)
		for word in confusion_set:
			confusion_set[word] +=(weighted_score(counts[word], total),)
		
		suggestions = sorted(confusion_set, key = lambda x: (-confusion_set[x][1], confusion_set[x][0]))
		
#		print(suggestions)
		
		if confusion_set[words[i]][1] == 0:
			index = suggestions.index(words[i])
			suggestions = suggestions[:index]
		elif confusion_set[suggestions[0]][1]*0.01 > confusion_set[words[i]][1]:
			index = suggestions.index(words[i])
			suggestions = suggestions[:index]
		else:
			suggestions = None
		
		print(suggestions)


if __name__ == '__main__':
	
	while True:
		sentence = input()
		start_time = time.time()
		detect(sentence)
		print(time.time() - start_time)
	




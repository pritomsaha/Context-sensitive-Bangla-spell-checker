import re, os
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
			file.write(ngram_str+"\t"+ str(ngrams[key])+"\n")

def main():
	stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')
	generate_ngram_count(1)
	generate_ngram_count(2)
	generate_ngram_count(3)


if __name__ == '__main__':
	main()


# unigrams = []
# bigrams = []
# trigrams = []
# fourgrams = []

# with open("sentences.txt") as infile:
# 	for line in infile:
# 		words = line.split()
# 		unigrams += words
# 		l = len(words)
# 		for i in range(0, l-1):
# 			bigrams.append((words[i], words[i+1]))

# 		for i in range(0, l-2):
# 			trigrams.append((words[i], words[i+1], words[i+2]))

# 		for i in range(0, l-3):
# 			fourgrams.append((words[i], words[i+1], words[i+2], words[i+3]))

# unigrams = Counter(unigrams)
# bigrams = Counter(bigrams)
# trigrams = Counter(trigrams)
# fourgrams = Counter(fourgrams)

# bigram_file = open('n_grams/bigrams.txt', 'a')
# trigram_file = open('n_grams/trigrams.txt', 'a')
# fourgram_file = open('n_grams/fourgrams.txt', 'a')

# for key in bigrams:
# 	bigram_file.write(key[0]+" "+key[1]+"	"+ str(bigrams[key])+"	"+ str(unigrams[key[0]])+"\n")

# for key in trigrams:
# 	trigram_file.write(key[0]+" "+key[1]+" "+key[2]+"	"+ str(trigrams[key])+"	"+ str(bigrams[(key[0], key[1])])+"\n")

# for key in fourgrams:
# 	fourgram_file.write(key[0]+" "+key[1]+" "+key[2]+" "+key[3]+"	"+ str(fourgrams[key])+"	"+ str(trigrams[(key[0], key[1], key[2])])+"\n")

# bigram_file.close()
# trigram_file.close()
# fourgram_file.close()
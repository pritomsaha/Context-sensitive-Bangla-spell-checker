import re, os
from stemmer.bangla_stemmer import bangla_stemmer
import logging
import multiprocessing
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

init_corpus_path = "../new_corp/initial_corp"
retrain_corpus_path = "../new_corp/retrain_corp"
stopwords_path = "../stop-words.txt"
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')

def  get_bn_wordlist(text, remove_stopwords = True):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [ bangla_stemmer().stemOfWord(w) for w in words if w not in stopwords]

	return (words)
	
class Sentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for file_name in os.listdir(self.dirname):
			with open(os.path.join(self.dirname, file_name), 'r', encoding = "utf-8") as infile:
				for line in infile:
					wordlist = get_bn_wordlist(line)
					if len(wordlist) >= 2:
						sentence = ' '.join(word for word in wordlist)
						yield sentence
						
if __name__ == '__main__':
	sentences = Sentences(init_corpus_path)
	with open("clean_corpus.txt", "a") as infile:
		for sentence in sentences:
			infile.write(sentence+"\n")

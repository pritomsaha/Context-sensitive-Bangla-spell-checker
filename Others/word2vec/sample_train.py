from stemmer.bangla_stemmer import bangla_stemmer
import re
import logging
import multiprocessing
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

stopwords_path = "../stop-words.txt"
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')

def get_bn_wordlist(text, remove_stopwords = True):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [w for w in words if w not in stopwords]
		
	return words
		
class Sentences(object):
	def __init__(self, file_name):
		self.file_name = file_name

	def __iter__(self):
		with open(self.file_name, 'r', encoding = "utf-8") as infile:
			for line in infile:
				wordlist = get_bn_wordlist(line)
				if len(wordlist) >= 2:
					yield wordlist
								
def  train(corpus_path):
	from gensim.models import word2vec
	sentences = Sentences(corpus_path)
	size = 100   # Word vector dimensionality                      
	min_count = 2   # Minimum word count                        
	workers = multiprocessing.cpu_count()       # Number of threads to run in parallel
	window = 5       # Context window size                                        
	sg = 0                                            
#	sample = 1e-3   # Downsample setting for frequent words

	print("Training model.......")
	model = word2vec.Word2Vec(sentences, workers=workers, \
            size=size, min_count = min_count, \
            window = window, sg = sg, hs=0, negative = 0)

	model.save("sample_model")
	
train("sample.txt")

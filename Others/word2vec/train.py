import re, os
from stemmer.bangla_stemmer import bangla_stemmer
import logging
import multiprocessing
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
init_corpus_path = "../corpus"
retrain_corpus_path = "../corpus"
stopwords_path = "../stop-words.txt"
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')

def  get_bn_wordlist(text, remove_stopwords = True):
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
			if os.path.isdir(file_name):
				continue
			with open(os.path.join(self.dirname, file_name), 'r', encoding = "utf-8") as infile:
				for line in infile:
					wordlist = get_bn_wordlist(line)
					if len(wordlist) >= 2:
						yield wordlist


def  train(corpus_path):
	from gensim.models import word2vec
	sentences = Sentences(corpus_path)
	size = 300   # Word vector dimensionality                      
	min_count = 5   # Minimum word count                        
	workers = multiprocessing.cpu_count()       # Number of threads to run in parallel
	window = 5       # Context window size                                        
	sg = 0
	hs = 1
	negative = 10                                            
#	sample = 1e-3   # Downsample setting for frequent words

	print("Training model.......")
	model = word2vec.Word2Vec(sentences, workers=workers, \
            size=size, min_count=min_count, \
            window=window, sg=sg, hs = hs, negative=negative)

	model.save("bn_model_sg"+str(sg)+"_win"+str(window)+"_hs"+str(hs)+"_negative"+str(negative))

# you can retrain model with more sentences
def retrain(corpus_path, model_path):
	from gensim.models import Word2Vec
	new_sentences = Sentences(corpus_path)
	model = Word2Vec.load(model_path)
	model.build_vocab(new_sentences, update=True)
	model.train(new_sentences, total_examples = model.corpus_count, epochs = model.iter)
	model.save(model_path)

def main():
	
	train(init_corpus_path)
#	retrain(retrain_corpus_path, "bn_model_sg0_win2_size300")

if __name__ == '__main__':
	main()
	

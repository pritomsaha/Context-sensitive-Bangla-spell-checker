import pandas as pa
import re
import nltk.data
from nltk.corpus import stopwords

bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)

def  get_wordlist(text, remove_stopwords = False):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.split()

	if remove_stopwords:
		print("i will do that")

	return (words)

def  train(sentences):
	import logging
	from gensim.models import word2vec
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
	
	num_features = 300    # Word vector dimensionality                      
	min_word_count = 40   # Minimum word count                        
	num_workers = 4       # Number of threads to run in parallel
	context = 10          # Context window size                                                                                    
	downsampling = 1e-3   # Downsample setting for frequent words

	print("Training model.......")
	model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

	model.init_sims(replace = True)
	model_name = "my_model"
	model.save(model_name)


def main():
	bn_wiki_file = open('ben_wikipedia_2016_30K-sentences.txt', 'r')
	sentences = []
	lines = bn_wiki_file.readlines()
	
	for line in lines:
		sentences.append(get_wordlist(line))

	train(sentences)


if __name__ == '__main__':
	main()
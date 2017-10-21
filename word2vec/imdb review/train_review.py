import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

import pandas as pa
from bs4 import BeautifulSoup
import re
import nltk.data
from nltk.corpus import stopwords

def review_to_wordlist(review, remove_stopwords = False):
	review_text = BeautifulSoup(review, "lxml").get_text()
	review_text = re.sub("[^a-zA-Z]", " ", review_text)
	words = review_text.lower().split()

	if remove_stopwords:
		stops = set(stopwords.words("english"))
		words = [w for w in words if w not in stops]

	return (words)

def  review_sentences(review, tokenizer, remove_stopwords = False):
	raw_sentences = tokenizer.tokenize(review.strip())
	sentences = []

	for raw_sentence in raw_sentences:
		if len(raw_sentence) > 0:
			sentences.append(review_to_wordlist(raw_sentence, remove_stopwords))

	return sentences

def  train_reviews(sentences):
	from gensim.models import word2vec
	num_features = 300    # Word vector dimensionality                      
	min_word_count = 40   # Minimum word count                        
	num_workers = 4       # Number of threads to run in parallel
	context = 10          # Context window size                                                                                    
	downsampling = 1e-3   # Downsample setting for frequent words

	print("Training model.......")
	model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

	# If you don't plan to train the model any further, calling 
	# init_sims will make the model much more memory-efficient.
	model.init_sims(replace = True)
	model_name = "review_model"
	model.save(model_name)

def  main():
	train = pa.read_csv('data/labeledTrainData.tsv', header = 0, delimiter = "\t", quoting = 3)
	test = pa.read_csv('data/testData.tsv', header = 0, delimiter = "\t", quoting = 3)
	unlabeled_train = pa.read_csv('data/unlabeledTrainData.tsv', header = 0, delimiter = "\t", quoting = 3)
	
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	sentences = []
	print("Parsing sentences from training set")
	for review in train['review']:
		sentences += review_sentences(review, tokenizer)

	sentences = []
	print("Parsing sentences from unlabeled set")
	for review in unlabeled_train['review']:
		sentences += review_sentences(review, tokenizer)

	train_reviews(sentences)

if __name__ == '__main__':
	main()

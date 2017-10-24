import re, os
from stemmer.bangla_stemmer import bangla_stemmer
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
stopwords = []
def  get_bn_wordlist(text, remove_stopwords = False):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split(" ")
	words = bangla_stemmer().stemOfWords(words)

	if remove_stopwords:
		words = [w for w in words if w not in stopwords]

	return (words)


def  get_en_wordlist(text, remove_stopwords = False):
	text = re.sub(r'[^a-zA-Z]', ' ', text)
	words = text.strip().lower().split(" ")

	if remove_stopwords:
		stops = set(stopwords.words("english"))
		words = [w for w in words if w not in stops]

	return (words)

def  train(sentences, model_name):
	from gensim.models import word2vec
	
	num_features = 300   # Word vector dimensionality                      
	min_word_count = 40   # Minimum word count                        
	num_workers = 4       # Number of threads to run in parallel
	context = 10        # Context window size                                                                                    
	downsampling = 1e-3   # Downsample setting for frequent words

	print("Training model.......")
	model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sg = 0, sample = downsampling)

	model.init_sims(replace = True)
	model.save(model_name)

# you can retrain model with more sentences
def retrain(new_sentences):
	from gensim.models import Word2Vec
	model = Word2Vec.load('model/my_model')
	model.build_vocab(new_sentences, update=True)
	model.train(new_sentences, total_examples = model.corpus_count, epochs = model.iter)

def get_sentences(corpus_path):
	folder_names = ['newspaper', 'web', 'wiki']
	sentences = []
	for folder_name in folder_names:
		for file_name in os.listdir(corpus_path+folder_name):
			with open(corpus_path+folder_name+'/'+file_name, 'r', encoding = "utf-8") as infile:
				for line in infile:
					sentences.append(get_bn_wordlist(line, True))
	return sentences

def main():
	stopwords = open('bn_stopwords.txt', 'r').read().split(',')
	corpus_path = "../../corpus/"
	sentences = get_sentences(corpus_path)
	train(sentences, "model/bn_model_sg0")

if __name__ == '__main__':
	main()
	
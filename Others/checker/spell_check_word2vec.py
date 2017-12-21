import re, time
from stemmer.bangla_stemmer import bangla_stemmer
from gensim.models import Word2Vec
from suggestion_generation import get_suggestions

bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
stopwords_path = "../stop-words.txt"
stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')
stemmer = bangla_stemmer()
model = Word2Vec.load("../word2vec/bn_model_sg0_win2_size300")

def get_bn_wordlist(text, remove_stopwords = True):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [w for w in words if w not in stopwords]

	return words

def excluded_words(words_1, words_2):
	for word in words_1:
		if word in words_2:
			words_2 = [w for w in words_2 if w != word]
	return words_2

def detect(sentence):
	wrong_list = {}
	word_list = get_bn_wordlist(sentence)
	words = []
	candidate_wrong_words = set()
	for word in word_list:
		if word not in model.wv.vocab:
			stemmed_word = stemmer.stemOfWord(word)
			if stemmed_word not in model.wv.vocab:
				candidate_wrong_words.add(word)
				words.append(word)
			else: words.append(stemmed_word)
		else: words.append(word)
	
	l = len(words)
	for i in range(l):
		confusion_set = get_suggestions(words[i])
		if words[i] not in candidate_wrong_words:
			confusion_set[words[i]] = (0.0, )
		
		suggestions = {}
		for word in confusion_set:
			_word = word
			if word not in model.wv.vocab:
				stemmed_word = stemmer.stemOfWord(word)
				if stemmed_word in model.wv.vocab:
					_word = stemmed_word
				else: _word = None
			
			similarity = None
			if _word:
				left_index = i-2 if i>1 else 0
				neighbor_words = excluded_words(candidate_wrong_words, words[left_index:i] + words[i+1:i+3])
				if len(neighbor_words):
					similarity = model.wv.n_similarity([_word], neighbor_words)
				
			if similarity:
				suggestions[word] = (similarity, confusion_set[word][0])
				

		sorted_suggestions = sorted(suggestions, key = lambda x: (-suggestions[x][0], suggestions[x][1] ))
		
		if len(sorted_suggestions) == 0:
			sorted_suggestions = None
		elif words[i] not in sorted_suggestions:
			sorted_suggestions = sorted_suggestions[:5]

		elif suggestions[words[i]][0] > 0.1*suggestions[sorted_suggestions[0]][0]:
			sorted_suggestions = None
		else:
			index = sorted_suggestions.index(words[i])
			sorted_suggestions = sorted_suggestions[:index]
		
		if sorted_suggestions:
			sorted_suggestions = sorted(sorted_suggestions, key = lambda x: suggestions[x][1])
		if sorted_suggestions:
			wrong_list[words[i]] = sorted_suggestions[:6]
	return wrong_list

if __name__ == '__main__':
	start_time = time.time()

	with open("sample.txt", "r") as infile:
		counter = 1
		for line in infile:
			split = line.split(">")
			if len(split) == 2:
				print(detect(split[0].strip()))
					
	print(time.time()-start_time)

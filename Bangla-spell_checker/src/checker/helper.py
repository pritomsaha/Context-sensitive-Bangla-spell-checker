import re, os
from django.conf import settings
from .phonetic_encoder import doublemetaphone_encode
from gensim.models import Word2Vec, KeyedVectors
from gensim.matutils import unitvec
import numpy as np
from django.conf import settings
from .stemmer.bangla_stemmer import bangla_stemmer
bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]+', re.UNICODE)
bn_al_pattern = re.compile(r'[\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]+', re.UNICODE)

def get_edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def get_encoded_word(word):
	return doublemetaphone_encode(word)

def weighted_distance(phonetic_edit_dist, edit_dist):
	return phonetic_edit_dist*0.6 + edit_dist*0.4

max_edit_distance = 1
def create_delete_list(word, delete_words, edit_distance = 1):
	l = len(word)
	if edit_distance > max_edit_distance or l <3 : return
	
	for c in range(l):
		new_word = word[:c] + word[c+1:]
		if new_word not in delete_words:
			delete_words.append(new_word)
			if len(new_word) > 2:
				create_delete_list(new_word, delete_words, edit_distance + 1)

def startup():
	dict_path = os.path.join(settings.BASE_DIR, "checker/dm_encwordlist.txt")
	model_path = os.path.join(settings.BASE_DIR, "checker/word2vec_model/bn_model_sg0_win5_hs1_negative0")
	stopwords_path = os.path.join(settings.BASE_DIR, "checker/stop-words.txt")
	model = KeyedVectors.load(model_path, mmap='r')
	wv = model.wv
	wordlist, delete_word_dic, encode_to_word_dic = set(), {}, {}
	with open(dict_path, 'r', encoding = "utf-8") as lines:
		for line in lines:
			encoded_word, real_word,  count = line.strip().split()
			wordlist.add(real_word)
			if encoded_word in encode_to_word_dic:
				encode_to_word_dic[encoded_word].append(real_word)
			else: 
				encode_to_word_dic[encoded_word] = [real_word]

			if encoded_word not in delete_word_dic:
				delete_word_dic[encoded_word] = []
			
			delete_words = []
			create_delete_list(encoded_word, delete_words)

			for item in delete_words:
				if item in delete_word_dic:
					delete_word_dic[item].append(encoded_word)
				else: delete_word_dic[item] = [encoded_word]
	
	stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')
	settings.wv = wv
	settings.wordlist = wordlist
	settings.delete_word_dic = delete_word_dic
	settings.encode_to_word_dic = encode_to_word_dic
	settings.stopwords = set(stopwords)


def get_confusion_set(input_word):
	suggestion_dic = {}
	encoded_input_word = get_encoded_word(input_word)
	encoded_input_word_len = len(encoded_input_word)
	listed_encoded_words = []
	if encoded_input_word in settings.delete_word_dic:
		if encoded_input_word in settings.encode_to_word_dic:
			listed_encoded_words.append(encoded_input_word)
			phonetic_edit_dist = 0
			for word in settings.encode_to_word_dic[encoded_input_word]:
				if word == input_word:
					continue
				weighted_edit_distance = weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word))
				suggestion_dic[word] = (weighted_edit_distance, )

		for encoded_word in settings.delete_word_dic[encoded_input_word]:
			if encoded_word not in listed_encoded_words:
				listed_encoded_words.append(encoded_word)
				phonetic_edit_dist = len(encoded_word) - encoded_input_word_len
				for word in settings.encode_to_word_dic[encoded_word]:
					weighted_edit_distance = weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word))
					suggestion_dic[word] = (weighted_edit_distance, )

	encoded_delete_words = []
	create_delete_list(encoded_input_word, encoded_delete_words)
	for encoded_delete_word in encoded_delete_words:
		if encoded_delete_word in settings.delete_word_dic:
			if encoded_delete_word in settings.encode_to_word_dic:
				if encoded_delete_word not in listed_encoded_words:
					listed_encoded_words.append(encoded_delete_word)
					phonetic_edit_dist = encoded_input_word_len - len(encoded_delete_word)
					for word in settings.encode_to_word_dic[encoded_delete_word]:
						weighted_edit_distance = weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word))
						suggestion_dic[word] = (weighted_edit_distance, )

			for encoded_word in settings.delete_word_dic[encoded_delete_word]:
				if encoded_word not in listed_encoded_words:
					listed_encoded_words.append(encoded_word)
					phonetic_edit_dist = get_edit_distance(encoded_word, encoded_input_word)
					for word in settings.encode_to_word_dic[encoded_word]:
						weighted_edit_distance = weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word))
						suggestion_dic[word] = (weighted_edit_distance, )
	return suggestion_dic




def cosine_similarity_score(word, context_words):
	if word not in settings.wv: return 0.0
	if len(context_words) == 0: return 0.0
	context_vectors = [settings.wv[w] for w in context_words]
	vector_mean = np.mean(np.array(context_vectors), axis=0, dtype=np.float64)
	dot_product = unitvec(settings.wv[word]).dot(unitvec(np.array(vector_mean)))
	return dot_product if dot_product>0 else 0.0
	
def detect_NonwordError(word, context_words):
	
	if word in settings.wordlist or bangla_stemmer.stemOfWord(word) in settings.wordlist:
		return None

	if word in settings.wv:
		if settings.wv.vocab[word].count > 99:
			return None

		stemmed_word = bangla_stemmer.stemOfWord(word)
		if stemmed_word in settings.wv:
			if settings.wv.vocab[stemmed_word].count > 99: 
				return None

	candidates = get_confusion_set(word)
	if not candidates:
		return None
	for candidate in candidates:
		candidates[candidate] +=(cosine_similarity_score(candidate, context_words),)
	
	return sorted(candidates, key = lambda x: (candidates[x][0]-candidates[x][1],))[:10]
	
def detect_RealwordError(word, context_words):
	if len(context_words) == 0:
		return None
	candidates = get_confusion_set(word)
	word_similarity = 0
	if word not in settings.wv:
		stemmed_word = bangla_stemmer.stemOfWord(word)
		if stemmed_word in settings.wv:
			word_similarity = cosine_similarity_score(stemmed_word, context_words)
	else:
		word_similarity = cosine_similarity_score(word, context_words)
	
	max_cosine_sim = 0
	for candidate in candidates:
		if candidate not in settings.wv:
			similarity = cosine_similarity_score(bangla_stemmer.stemOfWord(candidate), 	context_words)	
		else: similarity = cosine_similarity_score(candidate, context_words)
		max_cosine_sim = max(max_cosine_sim, similarity)
		candidates[candidate] +=(similarity,)
		
	if word_similarity >= 0.1*max_cosine_sim:
		return None
	candidates = {k: v for k, v in candidates.items() if v[1] >= 0.1*max_cosine_sim }
	if not candidates:
		return None
	return sorted(candidates, key = lambda x: (candidates[x][0], ))[:10]



def check(word_list):
	ln = len(word_list)
	for i in range(ln):
		word = word_list[i]
		isNonWord = True
		suggestions = None
		if word and word not in settings.stopwords:
			left_context = word_list[0:i]
			right_context = word_list[i+1:]
			context_words = []
			count = 0
			for w in reversed(left_context):
				if w not in settings.wv:
					stemmed_word = bangla_stemmer.stemOfWord(w)
					if stemmed_word in settings.wv:
						context_words.append(stemmed_word)
						count += 1
				else:
					context_words.append(w)
					count += 1
				if count == 2:
					break
			count = 0		
			for w in right_context:
				if w not in settings.wv:
					stemmed_word = bangla_stemmer.stemOfWord(w)
					if stemmed_word in settings.wv:
						context_words.append(stemmed_word)
						count += 1
				else:
					context_words.append(w)
					count += 1
				if count == 2:
					break
			
			suggestions = detect_NonwordError(word, context_words)
			if suggestions is None:
				isNonWord = False
				suggestions = detect_RealwordError(word, context_words)
		
		yield isNonWord, suggestions
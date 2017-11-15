import re, time
from gensim.models import Word2Vec
from suggestion_generation import get_suggestions

bn_char_pattern = re.compile(r'[^\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)
stopwords_path = "../stop-words.txt"
stopwords = open(stopwords_path, 'r').read().rstrip('\n').split(',')
model = Word2Vec.load("bn_model")

def  get_bn_wordlist(text, remove_stopwords = False):
	text = re.sub(bn_char_pattern, ' ', text)
	words = text.strip().split()
	if remove_stopwords:
		words = [w for w in words if w not in stopwords]

	return words

def detect(sentence):
	words = get_bn_wordlist(sentence)
	l = len(words)

	for i in range(l):
		# similarity = {}
		confusion_set = get_suggestions(words[i])
		confusion_set[words[i]] = (0.0, )
		for word in confusion_set:
			try:
				confusion_set[word] += (model.n_similarity([word], words[:i]+words[i+1:]), )
			except Exception as e:
				confusion_set[word] += (0.0, )
#		print(confusion_set)
		suggestions = sorted(confusion_set, key = lambda x: (-confusion_set[x][1], confusion_set[x][0]))
		
		if confusion_set[words[i]][1] > 0.01*confusion_set[suggestions[0]][1]:
			suggestions = None
		else:
			index = suggestions.index(words[i])
			suggestions = suggestions[:index]

		print(suggestions)

if __name__ == '__main__':
	start_time = time.time()
	detect("অন্ন কেউ নেই")
	print(time.time()-start_time)

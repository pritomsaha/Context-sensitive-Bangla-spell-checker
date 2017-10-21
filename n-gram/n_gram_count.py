from collections import Counter

unigrams = []
bigrams = []
trigrams = []
fourgrams = []

with open("sentences.txt") as infile:
	for line in infile:
		words = line.split()
		unigrams += words
		l = len(words)
		for i in range(0, l-1):
			bigrams.append((words[i], words[i+1]))

		for i in range(0, l-2):
			trigrams.append((words[i], words[i+1], words[i+2]))

		for i in range(0, l-3):
			fourgrams.append((words[i], words[i+1], words[i+2], words[i+3]))

unigrams = Counter(unigrams)
bigrams = Counter(bigrams)
trigrams = Counter(trigrams)
fourgrams = Counter(fourgrams)

bigram_file = open('n_grams/bigrams.txt', 'a')
trigram_file = open('n_grams/trigrams.txt', 'a')
fourgram_file = open('n_grams/fourgrams.txt', 'a')

for key in bigrams:
	bigram_file.write(key[0]+" "+key[1]+"	"+ str(bigrams[key])+"	"+ str(unigrams[key[0]])+"\n")

for key in trigrams:
	trigram_file.write(key[0]+" "+key[1]+" "+key[2]+"	"+ str(trigrams[key])+"	"+ str(bigrams[(key[0], key[1])])+"\n")

for key in fourgrams:
	fourgram_file.write(key[0]+" "+key[1]+" "+key[2]+" "+key[3]+"	"+ str(fourgrams[key])+"	"+ str(trigrams[(key[0], key[1], key[2])])+"\n")

bigram_file.close()
trigram_file.close()
fourgram_file.close()
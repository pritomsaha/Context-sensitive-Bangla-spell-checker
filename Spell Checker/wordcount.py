import re
file = open ("word_corpus.txt", "r")
text = file.readlines()
file.close()
word_freq ={ }

for line in text:
	words =re.split("[;*[]']", line.strip())
	for word in words:
		if word:
			count = word_freq.get(word, 0)
			word_freq[word] = count + 1

keys = word_freq.keys()

word_freq2 = { }
file = open ("dictionary.txt", "r")
text = file.readlines()
file.close()

file = open ("words_freq.txt", "w")

for line in text:
	word = line.strip()
	count = word_freq.get(word, 1)
	file.write(word+" "+str(count)+'\n')

file.close()
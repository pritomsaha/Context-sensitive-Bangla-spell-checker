import re

sentences_file = open("sentences.txt", 'a')
with open("corpus.txt") as infile:
	for line in infile:
		line = re.sub('[,/\[\]()><}{০-৯;]', '', line)
		sentences = re.split(r"\।|\?", line)
		sentences = sentences[:-1]
		for sentence in sentences:
			sentences_file.write("<s> "+sentence+" </s>\n")

sentences_file.close()

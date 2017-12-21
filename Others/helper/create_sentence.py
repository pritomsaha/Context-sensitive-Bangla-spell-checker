import re, os
def create_sentences(text):
	text = re.sub("\n", "", text)
	if len(text) == 0:
		return ""
	pattern = r"[\।|\?|;]+"
	sentences = re.split(pattern, text.rstrip(pattern))
	sentences = "\n".join(sentence.strip() for sentence in sentences)
	sentences += "\n"
	return sentences


if __name__ == '__main__':
	for file_name in os.listdir():
		if os.path.isdir(file_name):
			continue
		with open(file_name, "r") as infile:
			with open("New/"+file_name, "a") as outfile:
				for line in infile:
					sentences = create_sentences(line)
					outfile.write(sentences)

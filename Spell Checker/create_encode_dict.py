encodes = {"অ" :"o",  "আ": "a", "া": "a",  "ই": "i", "ঈ": "i", "ি":"i", "ী" : "i", "উ" : "u", "ঊ": "u", "ু": "u", "ূ": "u", "এ": "e", "ে": "e", "ঐ": "oi", "ৈ": "oi", "ও": "o", "ঔ": "ou","ৌ": "ou", "ক": "k", "খ": "k", "গ": "g", "ঘ": "g", "ঙ": "ng", "ং": "ng", "চ": "c", "ছ": "c", "য": "j", "জ": "j", "ঝ": "j", "ঞ": "n", "ট": "T", "ঠ": "T", "ড": "D", "ঢ": "D", "ঋ": "ri", "র": "r", "ড়": "r", "ঢ়": "r", "ন": "n", "ণ": "n", "ত": "t", "থ": "t", "দ": "d", "ধ": "d", "প": "p", "ফ": "p", "ব": "b", "ভ": "b", "ম": "m", "য়": "y", "ল": "l", "শ": "s", "স": "s", "ষ": "s", "হ": "h", "ঃ" : "h", "ৎ": "t"}
def get_encoded_word(word):
    encoded_word = ""
    for w in word:
        if w in encodes:
            encoded_word += encodes[w]
    return encoded_word

def main():
	file = open('words_freq.txt', 'r')
	lines = file.readlines()
	file.close()

	file = open('dict.txt', 'w')
	for line in lines:
		word, count = line.strip().split()
		encoded_word = get_encoded_word(word)
		file.write(encoded_word+" "+word+" "+count)
		file.write("\n")
	file.close()
if __name__ == '__main__':
	main()
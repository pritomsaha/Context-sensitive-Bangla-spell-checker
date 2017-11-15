import time
from phonetic_encoder import soundex_encode, doublemetaphone_encode
max_edit_distance = 1
dict_path = "../sd_encwordlist.txt"
doublemetaphone = True
if doublemetaphone:
	dict_path = "../dm_encwordlist.txt"

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
	return doublemetaphone_encode(word) if doublemetaphone else soundex_encode(word)

def weighted_distance(phonetic_edit_dist, edit_dist):
	return phonetic_edit_dist*0.6 + edit_dist*0.4


def create_delete_list(word, delete_words, edit_distance = 1):
	l = len(word)
	if edit_distance > max_edit_distance or l <3 : return
	
	for c in range(l):
		new_word = word[:c] + word[c+1:]
		if new_word not in delete_words:
			delete_words.append(new_word)
			if len(new_word) > 2:
				create_delete_list(new_word, delete_words, edit_distance + 1)

def generate_dictionary():
	dictionary, encode_to_word_map = {}, {}
	with open(dict_path, 'r', encoding = "utf-8") as lines:
		for line in lines:
			encoded_word, real_word,  count = line.strip().split()
			if encoded_word in encode_to_word_map:
				encode_to_word_map[encoded_word].append(real_word)
			else: 
				encode_to_word_map[encoded_word] = [real_word]

			if encoded_word not in dictionary:
				dictionary[encoded_word] = []
			
			delete_words = []
			create_delete_list(encoded_word, delete_words)

			for item in delete_words:
				if item in dictionary:
					dictionary[item].append(encoded_word)
				else: dictionary[item] = [encoded_word]
	return dictionary, encode_to_word_map


def get_suggestions(input_word):
	suggestion_dic = {}
	encoded_input_word = get_encoded_word(input_word)
	encoded_input_word_len = len(encoded_input_word)

	listed_encoded_words = []
	if encoded_input_word in dictionary:
		if encoded_input_word in encode_to_word_map:
			listed_encoded_words.append(encoded_input_word)
			for word in encode_to_word_map[encoded_input_word]:
				typo_edit_distance = get_edit_distance(input_word, word)
				if typo_edit_distance > max_edit_distance:
					continue
				suggestion_dic[word] = (weighted_distance(0, typo_edit_distance), )

		for encoded_word in dictionary[encoded_input_word]:
			if encoded_word not in listed_encoded_words:
				listed_encoded_words.append(encoded_word)
				phonetic_edit_dist = len(encoded_word) - encoded_input_word_len
				for word in encode_to_word_map[encoded_word]:
					typo_edit_distance = get_edit_distance(input_word, word)
					if typo_edit_distance > max_edit_distance:
						continue
					suggestion_dic[word] = (weighted_distance(phonetic_edit_dist, typo_edit_distance), )

	encoded_delete_words = []
	create_delete_list(encoded_input_word, encoded_delete_words)
	for encoded_delete_word in encoded_delete_words:
		if encoded_delete_word in dictionary:
			if encoded_delete_word in encode_to_word_map:
				if encoded_delete_word not in listed_encoded_words:
					listed_encoded_words.append(encoded_delete_word)
					phonetic_edit_dist = encoded_input_word_len - len(encoded_delete_word)
					for word in encode_to_word_map[encoded_delete_word]:
						typo_edit_distance = get_edit_distance(input_word, word)
						if typo_edit_distance > max_edit_distance:
							continue
						suggestion_dic[word] = (weighted_distance(phonetic_edit_dist, typo_edit_distance), )

			for encoded_word in dictionary[encoded_delete_word]:
				if encoded_word not in listed_encoded_words:
					listed_encoded_words.append(encoded_word)
					phonetic_edit_dist = get_edit_distance(encoded_word, encoded_input_word)
					for word in encode_to_word_map[encoded_word]:
						typo_edit_distance = get_edit_distance(input_word, word)
						if typo_edit_distance > max_edit_distance:
							continue
						suggestion_dic[word] = (weighted_distance(phonetic_edit_dist, typo_edit_distance), )
	return suggestion_dic

dictionary, encode_to_word_map = generate_dictionary()
# def main():
# 	start_time = time.time()
# 	print(get_suggestions("অংকন"))
# 	print(time.time()-start_time)

# if __name__ == '__main__':
# 	main()


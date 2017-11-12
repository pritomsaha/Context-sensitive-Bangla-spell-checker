import time
from phonetic_encoder import soundex_encode, doublemetaphone_encode
max_edit_distance = 1
dict_path = "../sd_encwordlist.txt"
doublemetaphone = True
if doublemetaphone:
	dict_path = "../dm_encwordlist.txt"
def get_edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    # if abs(m-n)>max_edit_distance: return max_edit_distance+1
    dp = [[0 for v in range(m+1) ] for __ in range(n+1) ]
    for i in range(m+1):
        dp[0][i] = i
    for i in range(n+1):
        dp[i][0] = i
    for j in range(1, m+1):
        for i in range(1, n+1):
            dp[i][j] = min(dp[i-1][j-1] + (word1[j-1]!=word2[i-1]) , dp[i-1][j]+1, dp[i][j-1]+1)
            
    return dp[n][m]

def get_encoded_word(word):
	return doublemetaphone_encode(word) if doublemetaphone else soundex_encode(word)

def create_delete_list(word, delete_words, edit_distance = 1):
	l = len(word)
	if edit_distance > max_edit_distance or l <3 : return
	
	for c in range(l):
		new_word = word[:c] + word[c+1:]
		if new_word not in delete_words:
			delete_words.append(new_word)
			if len(new_word) > 2:
				create_delete_list(new_word, delete_words, edit_distance + 1)

def weighted_distance(phonetic_edit_dist, edit_dist):
	return phonetic_edit_dist*0.6 + edit_dist*0.4

def generate_dictionary():
	dictionary, encode_to_word_map = {}, {}
	with open(dict_path, 'r', encoding = "utf-8") as lines:
		for line in lines:
			encoded_word, real_word,  count = line.strip().split()
			if encoded_word in encode_to_word_map:
				encode_to_word_map[encoded_word].append((real_word, int(count)))
			else: 
				encode_to_word_map[encoded_word] = [(real_word, int(count))]

			if encoded_word not in dictionary:
				dictionary[encoded_word] = []
			
			delete_words = []
			create_delete_list(encoded_word, delete_words)

			for item in delete_words:
				if item in dictionary:
					dictionary[item].append(encoded_word)
				else: dictionary[item] = [encoded_word]
	return dictionary, encode_to_word_map

def get_suggestion(dictionary, encode_to_word_map, input_word):
	suggestion_dic = {}
	encoded_input_word = get_encoded_word(input_word)
	encoded_input_word_len = len(encoded_input_word)
	listed_encoded_words = []
	if encoded_input_word in dictionary:
		if encoded_input_word in encode_to_word_map:
			listed_encoded_words.append(encoded_input_word)
			for word_tuple in encode_to_word_map[encoded_input_word]:
				suggestion_dic[word_tuple[0]] = (word_tuple[1], weighted_distance(0, get_edit_distance(input_word, word_tuple[0])))

		for encoded_word in dictionary[encoded_input_word]:
			if encoded_word not in listed_encoded_words:
				listed_encoded_words.append(encoded_word)
				phonetic_edit_dist = len(encoded_word) - encoded_input_word_len
				for word_tuple in encode_to_word_map[encoded_word]:
					suggestion_dic[word_tuple[0]] = (word_tuple[1], weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word_tuple[0])))
	
	encoded_delete_words = []
	create_delete_list(encoded_input_word, encoded_delete_words)
	for encoded_delete_word in encoded_delete_words:
		if encoded_delete_word in dictionary:
			if encoded_delete_word in encode_to_word_map:
				if encoded_delete_word not in listed_encoded_words:
					listed_encoded_words.append(encoded_delete_word)
					phonetic_edit_dist = encoded_input_word_len - len(encoded_delete_word)
					for word_tuple in encode_to_word_map[encoded_delete_word]:
						suggestion_dic[word_tuple[0]] = (word_tuple[1], weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word_tuple[0])))

			else:
				for encoded_word in dictionary[encoded_delete_word]:
					if encoded_word not in listed_encoded_words:
						listed_encoded_words.append(encoded_word)
						phonetic_edit_dist = get_edit_distance(encoded_word, encoded_input_word)
						for word_tuple in encode_to_word_map[encoded_word]:
							suggestion_dic[word_tuple[0]] = (word_tuple[1], weighted_distance(phonetic_edit_dist, get_edit_distance(input_word, word_tuple[0])))

	return sorted(suggestion_dic, key = lambda x: (suggestion_dic[x][1], -suggestion_dic[x][0]))


def test(file_name, dictionary, encode_to_word_map):
	count = {"in_first": 0, "in_third": 0, "in_tenth": 0, "in_all": 0}
	total_words = 0
	with open(file_name, 'r', encoding = "utf-8") as infile:
		lines = infile.readlines()
		total_words = len(lines)
		for line in lines:
			wrong, correct = line.split('-')
			correct = correct.strip()
			suggestions = get_suggestion(dictionary, encode_to_word_map, wrong.strip())

			if correct in suggestions:
				count["in_all"]+=1
				if correct in suggestions[:10]:
					count["in_tenth"]+=1
					if correct in suggestions[:3]:
						count["in_third"]+=1
						if correct in suggestions[:1]:
							count["in_first"]+=1

	for c in count:
		count[c] = (count[c]/total_words)*100.0
	print(count)



def main():
	start_time = time.time()
	dictionary, encode_to_word_map = generate_dictionary()
	print((time.time() - start_time))
	start_time = time.time()
	test("test.txt", dictionary, encode_to_word_map)
	print((time.time() - start_time))
	
	
if __name__ == '__main__':
	main()
#	print(soundex_encode("অনার্য"), doublemetaphone_encode("অনার্য"))

# accuracy using wiki data

# max_phonetic edit distance = 2
	# soundex
	# {'in_third': 94.12698412698413, 'in_all': 98.09523809523809, 'in_first': 77.77777777777779, 'in_tenth': 96.82539682539682}
	
	# doublemetaphone
	# {'in_all': 98.09523809523809, 'in_tenth': 97.46031746031746, 'in_third': 95.55555555555556, 'in_first': 79.84126984126985}
	
# max_phonetic edit distance = 1
	# soundex
	# {'in_all': 94.76190476190476, 'in_third': 93.33333333333333, 'in_first': 77.61904761904762, 'in_tenth': 94.6031746031746}
	# doublemetaphone
	# {'in_third': 94.12698412698413, 'in_first': 79.36507936507937, 'in_tenth': 95.23809523809523, 'in_all': 95.3968253968254}

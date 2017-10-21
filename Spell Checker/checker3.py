import time

max_edit_distance = 2

def get_edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    if abs(m-n) >2: return 3
    dp = [[0 for v in range(m+1) ] for __ in range(n+1) ]
    for i in range(m+1):
        dp[0][i] = i
    for i in range(n+1):
        dp[i][0] = i
    for j in range(1, m+1):
        for i in range(1, n+1):
            dp[i][j] = min(dp[i-1][j-1] + (word1[j-1]!=word2[i-1]) , dp[i-1][j]+1, dp[i][j-1]+1)
            
    return dp[n][m]

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
	file = open('words_freq.txt', 'r')
	lines = file.readlines()
	file.close()
	dictionary = {}
	for line in lines:
		word, count = line.strip().split()
		if word in dictionary:
			dictionary[word] =(dictionary[word][0], int(count))
		else:
			dictionary[word] = ([], int(count))

		delete_words = []
		create_delete_list(word, delete_words)

		for item in delete_words:
			if item in dictionary:
				dictionary[item][0].append(word)
			else: dictionary[item] = ([word], 0)
	return dictionary

def get_suggestion(dictionary, input_word):
	suggestion_dic = {}
	if input_word in dictionary:
		if dictionary[input_word][1]>0:
			suggestion_dic[input_word] = (dictionary[input_word][1], 0)
			for word in dictionary[input_word][0]:
				suggestion_dic[word] = (dictionary[word][1], len(word)-len(input_word))
			return suggestion_dic
		else:
			for word in dictionary[input_word][0]:
				if word not in suggestion_dic:
					suggestion_dic[word] = (dictionary[word][1], len(word)-len(input_word))
	
	delete_words = []
	create_delete_list(input_word, delete_words)
	for delete_word in delete_words:
		if delete_word in dictionary:
			if dictionary[delete_word][1] > 0:
				if delete_word not in suggestion_dic:
					suggestion_dic[delete_word] = (dictionary[delete_word][1], len(input_word) - len(delete_word))
				for word in dictionary[delete_word][0]:
					if word not in suggestion_dic:
						edit_distance = get_edit_distance(word, input_word)
						if edit_distance <= max_edit_distance:
							suggestion_dic[word] = (dictionary[word][1], edit_distance)
			else:
				for word in dictionary[delete_word][0]:
					if word not in suggestion_dic:
						edit_distance = get_edit_distance(word, input_word)
						if edit_distance <= max_edit_distance:
							suggestion_dic[word] = (dictionary[word][1], edit_distance)
	return suggestion_dic


def main():
    dictionary = generate_dictionary()
    file = open('test.txt', 'r')
    lines = file.readlines()
    file.close()
    count=0
    first_count = 0
    third_count = 0
    c=0
    for line in lines:
        wrong, correct = line.split('-')
        correct = correct.strip()
        suggestion_dic = get_suggestion(dictionary, wrong.strip())
        if correct in dictionary and dictionary[correct][1]>0:
            suggestions = sorted(suggestion_dic, key = lambda x: (suggestion_dic[x][1], -suggestion_dic[x][0]))
            if correct in suggestions:
                count+=1
                if correct in suggestions[:3]:
                    third_count  += 1
                    if correct == suggestions[0]:
                        first_count  += 1
        else:
            c+=1
    print(c, count, third_count,  first_count)

if __name__ == '__main__':
	main()
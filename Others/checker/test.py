from spell_check import *

def test_nonword(file_name = "wrong_words.txt"):
	count = {"in_first": 0, "in_third": 0, "in_tenth": 0, "in_all": 0}
	total_words = 0
	with open(file_name, 'r', encoding = "utf-8") as infile:
		lines = infile.readlines()
		total_words = len(lines)
		for line in lines:
			wrong, correct = line.split('-')
			correct = correct.strip()
			suggestion_dic = get_confusion_set(wrong.strip())
			suggestions = sorted(suggestion_dic, key = lambda x: (suggestion_dic[x][0], ))

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

def clean_test_corp():
	from random import randint

	with open("test_corpus.txt", "r") as infile:
		counter = 0
		clean_file = open("clean_testcorp.txt", "w")
		result_file = open("result.txt", "w")
		line_num = 0
		for line in infile:
			words = get_bn_wordlist(line)
			words_str = ""
			for i in range(len(words)):
				word = words[i]
				if counter == 20:
					candidates = get_confusion_set(word)
					candidates = list(candidates.keys())
					ln = len(candidates)
					if ln == 0:
						words_str += word+" "
						continue
					counter = 0
					while True:
						r = randint(0,ln-1)
						if candidates[r] != word and candidates[r] not in stopwords:
							t = word==candidates[r]
							if t:
								print(t)
								return

							result_file.write(candidates[r]+" "+word+" "+str(line_num)+" "+str(i)+"\n")
							word = candidates[r]
							break
						if ln == 1:
							break


				counter += 1
				words_str += word+" "
			
			clean_file.write(words_str.strip()+"\n")
			line_num += 1
		clean_file.close()
		result_file.close()
		
def save_test_result():
	with open("clean_testcorp.txt", "r") as infile:
		line_num = 0
		test_result_f = open('test_result.txt', 'w')
		for line in infile:
			word_list = line.strip().split()
			for i, suggestions in check(word_list):
				if suggestions:
					suggestions_str = ",".join(s for s in suggestions)
					test_result_f.write(word_list[i]+" "+" "+str(line_num)+" "+str(i)+" "+suggestions_str+"\n")
			line_num += 1
		test_result_f.close()
		
	
		
def get_final_result():
	results = []
	real_words = []
	num_error = 0
	error_detected = 0
	true_positive = 0
	with open("result.txt", 'r') as infile:
		
		for line in infile:
			rs = line.split()
			real_words.append(rs[1])
			rs = rs[:1]+rs[2:]
			rs_str = ''.join(r for r in rs)
			results.append(rs_str)
			num_error += 1
	
#	print(real_words)
#	return
	suggest_acc = {}	
	with open("test_result.txt", 'r') as infile:
		
		for line in infile:
			split = line.split()
			trs = split[:3]
			suggestions = split[3].split(",")
			trs_str = ''.join(t for t in trs)
			if trs_str in results:
				true_positive += 1
				index = results.index(trs_str)
				if real_words[index] in suggestions[:1]:
					suggest_acc[1] = suggest_acc.get(1, 0) + 1
				if real_words[index] in suggestions[:3]:
					suggest_acc[3] = suggest_acc.get(3, 0) + 1
				if real_words[index] in suggestions[:5]:				
					suggest_acc[5] = suggest_acc.get(5, 0) + 1
			error_detected += 1
			
	precision = true_positive/error_detected
	recall = true_positive/num_error
			
	print("true_positive:",true_positive, "error_detected:", error_detected, "num_error:", num_error)
	print("precision : ",precision)
	print("recall :", recall)
#	print(suggest_acc)
	
clean_test_corp()
save_test_result()
get_final_result()	
#test_nonword()

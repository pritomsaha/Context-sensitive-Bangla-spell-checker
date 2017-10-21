from TST import TST
from _io import open
letters = "অআইঈউঊঋএঐওঔকখখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁািীুূৃেৈো্"
letters2 = "ঁািীুূৃেৈো্"
letters3 = "ৎংঃঁািীুূৃেৈো্"
def isValid(word):
    if len(word) == 0: return False
    if word[0] in letters3:
        return False
    prev = '???'
    for letter in word:
        if letter in letters2 and prev in letters2:
            return False
        prev = letter
    return True

def edit1(word):
	l = len(word)
	splits = [(word[:i], word[i:]) for i in range(l+1)]
	deletes = {L + R[1:] for L, R in splits if R and isValid(L + R[1:])}
	replaces = {L + c + R[1:] for L, R in splits if R for c in letters if c!=R[0] and isValid(L + c + R[1:])}
	inserts = {L + c + R for L, R in splits for c in letters if isValid(L + c + R)}
	return deletes | replaces | inserts

def get_possible_words(word):
    edit1_words = edit1(word)
    edit2_words = {e2 for e1 in edit1_words for e2 in edit1(e1)}
    return edit1_words | edit2_words

def get_suggestion(input_word, tst):
    possible_words = get_possible_words(input_word)
    suggestion_words = []
    for word in possible_words:
        prior = tst.search(word)
        if prior is not None:
            suggestion_words.append((prior, word))
    return suggestion_words
    
if __name__ == '__main__':
    dic_file = open('words_freq.txt', 'r')
    dic_words = dic_file.readlines()
    dic_file.close()
    tst = TST()
    for line in dic_words:
        word, count = line.strip().split()
        tst.insert(word, int(count))
    
    file = open('test.txt')
    lines = file.readlines()
    file.close()
    success_count = 0
    for line in lines:
        wrong_word, correct_word = line.strip().split('-')
        suggestions = get_suggestion(wrong_word.strip(), tst)
        if correct_word.strip() in (item[1] for item in suggestions):
            success_count += 1
        print(success_count)
    print(success_count)
        

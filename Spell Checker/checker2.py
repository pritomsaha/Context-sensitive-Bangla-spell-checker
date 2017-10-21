import time
encodes = {"অ" :"o",  "আ": "a", "া": "a",  "ই": "i", "ঈ": "i", "ি":"i", "ী" : "i", "উ" : "u", "ঊ": "u", "ু": "u", "ূ": "u", "এ": "e", "ে": "e", "ঐ": "oi", "ৈ": "oi", "ও": "o", "ঔ": "ou","ৌ": "ou", "ক": "k", "খ": "k", "গ": "g", "ঘ": "g", "ঙ": "ng", "ং": "ng", "চ": "c", "ছ": "c", "য": "j", "জ": "j", "ঝ": "j", "ঞ": "n", "ট": "T", "ঠ": "T", "ড": "D", "ঢ": "D", "ঋ": "ri", "র": "r", "ড়": "r", "ঢ়": "r", "ন": "n", "ণ": "n", "ত": "t", "থ": "t", "দ": "d", "ধ": "d", "প": "p", "ফ": "p", "ব": "b", "ভ": "b", "ম": "m", "য়": "y", "ল": "l", "শ": "s", "স": "s", "ষ": "s", "হ": "h", "ঃ" : "h", "ৎ": "t"}

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

def get_encoded_word(word):
    encoded_word = ""
    for w in word:
        if w in encodes:
            encoded_word += encodes[w]
    return encoded_word

def get_suggestions(word, dic_words, encoded_words):
    suggestions = []
    encoded_word = get_encoded_word(word)
    for i in range(total_words):
        phonetic_edit_distance = 0 if encoded_word == encoded_words[i] else get_edit_distance(encoded_word, encoded_words[i],)
        if phonetic_edit_distance>2: continue
        normal_edit_distance = get_edit_distance(word, dic_words[i])
        score = 0.7*phonetic_edit_distance + 0.3*normal_edit_distance
        if score <= 2:
            suggestions.append((score, dic_words[i]))
    return sorted(suggestions)

if __name__ == '__main__':
    dic_file = open('dictionary.txt', 'r')
    lines = dic_file.readlines()
    dic_file.close()
    dic_words = []
    encoded_words = []

    for line in lines:
        word = line.strip().strip('‌')
        dic_words.append(word)
        encoded_words.append(get_encoded_word(word))
    total_words = len(dic_words)
    
#     print(get_encoded_word("শ্রদ্ধাভাজনীয়"))
#     print(get_encoded_word("শ্রদ্ধাভাজন"))
#     print(get_edit_distance("শ্রদ্ধাভাজনীয়", "শ্রদ্ধাভাজন"))
#     start_time = time.time()
    file = open('test.txt', 'r')
    lines = file.readlines()
    file.close()
    count = 0
    print(get_suggestions("শ্রদ্ধাভাজনীয়", dic_words, encoded_words))
    for line in lines:
        wrong, correct = line.split('-')
        if correct.strip() in dic_words:
            count += 1 
    print(count)
#         suggestions = get_suggestions(wrong.strip(), dic_words, encoded_words)
#         if suggestions:
#             if suggestions[0][1] == correct.strip():
#                 count += 1
#         else: print(correct.strip())
#     print(count)
#     suggestions = get_suggestions("দৈনতা", dic_words, encoded_words)  
#     print(time.time() - start_time)
    
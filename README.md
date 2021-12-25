# Context-sensitive-Bangla-spell-checker
Software Project Lab 3

## Proposed context-sensitive spell checking approach and implementation
In Spell Checker, two major steps are misspelling detection and then providing suggestions of most likely valid words. The proposed spell-checking approach can detect non-word and real-word errors in the text and provide suggestions. There are challenges for detecting both of the errors mentioned above. For detecting, if a word is a non-word error, it is just checked if the word is in the lexicon. For this project, we have generated a lexicon with 112802 Bangla words. If a word is not in the
lexicon, the stemmed version may be in the lexicon. For
this, a rule-based Bangla stemmer has been used to get the stem of a Bangla word which takes a file with some defined rules for stemming a given word. For example, for the word "কাজটি", the stemmed version of this word will be "কাজ". If the stemmed word also is not in the
lexicon, then the word is marked as a non-word error, and for this, valid suggestions should be generated.

In the real-word, there are contextual errors that depend on the word's context. To find if a word is contextually inappropriate in a sentence, we can not think about the word in an isolated way; the words surrounding the word should be in the calculation to detect a real-word error. Here word vectors generated before using word2vec models will be used. First, a confusion set of candidate words set is generated, and how
this set is produced that will be explained in detail in the next section of the suggestion generation.
At first, the cosine similarity of context words with the given word and all the confusion set members are calculated. Cosine similarity is calculated by taking the dot product of the unit vectors of any two words' vectors. Before calculating the dot product, vectors of context
words are averaged into one single vector. Here for context words, we have chosen the left two words and right two words of the given word. After calculating cosine similarity, we will get a similarity score between -1 and 1. To get a non-negative value, if a cosine similarity value is less than 0, we turn them to 0(zero). 

However, it may happen that the given word to be detected, or any word in the confusion set may not be in the vocabulary set of word vectors. For this, we produced the stem of this word, and if the stemmed word is not also in the vocabulary of word vectors, we set the cosine similarity for that word
as 0(zero). The same problem may happen for context words, and we use the same technique of stemming the word, getting the vector of the stemmed word, and calculating the average o context word vectors.
If the stemmed word does not have the corresponding vector, then we ignore the word and move to the same direction for another word and apply the same technique for this word. If there are no context words on the left side or we do not get any context word vector, we ignore detecting real-word error and go to the next word. 

After performing the above calculation, we have the cosine similarity value of all words in the confusion set and the word to be detected with the context words. The question is how we use these cosine similarity values to detect the given word as if it is contextually correct or inappropriate.  For this, we first find the max similarity value within words in the confusion set and use a threshold value to compare this max value with the similarity score of the given word. Here the threshold value is used 0.1 as an experiment and multiply this threshold value with the similarity score of the given word and compare the multiplied result with the max value of cosine similarity within the confusion set. If the result is less than the max similarity score, we marked the given word as a real-word error, suggesting the most likely valid words. After detecting a word as misspelled, the suggestion of most likely valid words is generated. For both non-word and real-word errors, the same suggestion generation technique has been used. Here, words in the confusion set are generated from phonetically similar words or generated by one edit distance. The double Metaphone phonetic encoding technique has been used to encode words so that phonetically related words would have the same or nearly distanced encoding. For example, after double Metaphone encoding of অনয্ and অন্ will have the same encoding 'onn'. In the pre-calculation step, the encoded word and the original Bangla word of every dictionary term are associated and stored in a data structure. After this, there will be a list of original Bangla words mapped with the encoded-word. 

Suppose we use conventional possible terms generation up to 1 edit distance of input word by deleting, transporting, replacing, and inserting, then for edit distance one and input word length of l. In that case, it needs l deletions, l − 1 transposition, l + 1 insertion, l alterations. It is computationally expensive if we want to pre-calculate possible terms for one edit distance for all dictionary terms. To improve the speed of possible terms generation of a certain edit distance, we have used the technique of FAROO's Symmetric Delete Spelling Correction. More specifically, all terms with up to one edit distance (deletes only) of every phonetically encoded word in the dictionary have been produced in the pre-calculation step. These deleted words have been associated with their original encoded term and stored in
a data structure. For example for a delete encoded delete word 'on' the associated original encoded words are' onn',' ont',' osn',' oln',' onD',' onn',' kon',' onu',' okn',' ojn',' ond',' ojn',' onl',' omn',' ont',' oyn',' onr'. From previous Bangla word and encoded word association we can get all the original Bangla words from all of these encoded words. Now for any input word, the following steps are used to produce the confusion set:
First, the encoded word of the input word is produced using the same double Metaphone algorithm. An empty confusion set is initialized.
The encoded input word is then checked in the previously stored original Bangla word and encoded-word association. If there is an entry with this encoded input word, then the associated all Bangla words with this encoded-word are added to the confusion set.
Then all the words with one edit distance using only delete operations are
obtained, and for each of these words, it is checked if it exists in the previously stored delete word and encoded word association and if it exists then all the mapped encoded words are retrieved.
At last, from all the retrieved encoded words, original Bangla words are obtained and added to the confusion set. After generating the confusion set, we have to set some criteria to sort these words so that most likely words should be at the top of the suggestion list. Typographic edit distance, Phonetic edit distance, and Cosine similarity these three 
parameters are used for ranking the suggestion.

## Corpus generation
A corpus or text corpus is a large and structured set of texts. As in the proposed system, a real-word error will be detected, which depends on the context knowledge of the word based on surrounding words in the text. For knowing the context of the word, the similarity of a word in a sentence is used. We used word2vec for representing Bangla words in vector form so that using some mathematical vector operation, we can find out the proximity of two or more words. For creating the vector representation of words, we need a large corpus of text. So for training, a model for Bangla language, a large set of text is collected to make a corpus of Bangla language. From different sources like Wikipedia, Bangla newspaper, Bangla literature, Bangla texts are collected. A program was written for crawling text from the website called ebanglalibrary. For other news crawl and Wikipedia data, available data for Bangla from the website Leipzig Corpora Collection are collected. Here, a python library Request is used to get the source of a webpage and python parser library Beautiful Soup (BS4) to parse HTML and XML documents. After collecting text, those were split into sentences.

## Training corpus using word2vec
As mentioned before, for learning word vectors, word2vec is used to train the generated corpus of Bangla text. Word vector is simply a weighted vector of a specified dimension where every element in the vector represents weight. In word2vec, an unlabeled training corpus is given; by learning from this corpus, a vector for each unique in the corpus is produced in such a way that the vector can encode the semantic information of a word. We can easily measure the similarity between two words from these vectors by calculating the cosine similarity of the corresponding word vectors of those words. Words with nearly closed semantic meanings will have similarity vectors in cosine similarity. 

We used Gensim python library gensim.models.word2vec function
to train the model. This function takes a list of sentences as input, where a sentence is a list of words. Before training, some preprocessing(cleaning) was done on every sentence in the corpus. First, every character except Bangla alphabets (only alphabet, not numerical) is removed from the sentence. Then Bangla stop-words(commonly used words) have been removed from the sentence. Here as hidden layer size 300 has been, which gives comparatively good result and the window size of 5 has been used in training, which means in the time of training in input layer five left and five right context words will be used to learn the model. Here several models have been trained using both softmax function and negative sampling. The specified function will return a model which can be used to retrain with more sentences at any time.

## How to Use
Prerequisites: Git, Python-3 Django 1.11.2 with the virtual environment.
Following are the steps for running the project. 
##### a) go to Bangla-spell_checker directory and activate virtual environment
    source bin/activate
##### b) go to Bangla-spell_checker/src directory and run the project 
    python manage.py runserver [ip:port](default is localhost:8000)
The project will be run in localhost and type the ip and port in the browser and continue

## Helpful Links
* For the tutorial about word2vec model architecture, use this link: http://mccormickml.com/2016/04/27/word2vec-resources/

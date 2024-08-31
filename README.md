# Context-sensitive-Bangla-spell-checker
Software Project Lab 3

## Proposed Context-Sensitive Spell-Checking Approach and Implementation

### Overview of Spell Checking Process

A spell checker typically involves two primary steps: **misspelling detection** and **suggestion generation** for valid alternatives. The proposed approach enhances this process by addressing both **non-word errors** and **real-word errors** in Bangla text, ensuring accurate detection and relevant suggestions.

### Detecting Non-Word and Real-Word Errors

#### Non-Word Error Detection

To identify non-word errors, each word in the text is checked against a comprehensive lexicon containing 112,802 Bangla words. If a word is not found in the lexicon, its stemmed version is then examined using a rule-based Bangla stemmer. For instance, the word "কাজটি" is stemmed to "কাজ." If the stemmed word also does not exist in the lexicon, the original word is marked as a non-word error, necessitating the generation of valid suggestions.

#### Real-Word Error Detection

Real-word errors involve contextually inappropriate words that are valid Bangla words but incorrect within their specific context. Detecting these errors requires analyzing the surrounding words rather than evaluating the target word in isolation. To achieve this, word vectors generated using Word2Vec models are utilized. The process involves the following steps:

1. **Contextual Similarity Calculation**: 
   - The cosine similarity between the target word and its surrounding context words is computed. Specifically, the left two and right two words of the target word are averaged into a single context vector.
   - Cosine similarity, calculated as the dot product of unit vectors, ranges between -1 and 1. Negative values are set to zero to ensure non-negative similarity scores.

2. **Handling Out-of-Vocabulary Words**:
   - If the target word or any word in the confusion set is not present in the Word2Vec vocabulary, the stemmed version is used. If the stemmed word is also absent, its cosine similarity is set to zero.
   - For context words lacking vectors, stemming is applied. Words without valid stemmed vectors are ignored. If no valid context words remain on the left side, real-word error detection for that word is skipped.

3. **Error Detection Criterion**:
   - After computing cosine similarities for all confusion set members, the maximum similarity value within the confusion set is compared against a threshold derived from the target word's similarity score (threshold set to 0.1 experimentally).
   - If the maximum similarity in the confusion set exceeds the threshold-adjusted similarity of the target word, the target word is flagged as a real-word error, and suggestions are generated accordingly.

### Suggestion Generation for Misspelled Words

Once a word is identified as misspelled—either as a non-word or a real-word error—the system generates suggestions for correction using a confusion set. The confusion set comprises phonetically similar words and words within one edit distance from the target word. The Double Metaphone phonetic encoding technique is employed to group phonetically related words. For example, both "অনয্" and "অন্" are encoded as 'onn', facilitating the association of phonetically similar words.

To efficiently generate possible terms, the **Symmetric Delete Spelling Correction** method is utilized. This involves precomputing all possible deletions (up to one edit distance) of phonetically encoded words and storing these in a data structure for quick lookup. For instance, the delete-encoded word 'on' might map to several original encoded words such as 'onn', 'ont', 'osn', etc. During suggestion generation, the input word is encoded using Double Metaphone, and both direct matches and one-deletion variants are used to retrieve potential corrections from the precomputed associations.

### Ranking Suggestions

Suggestions are ranked based on three key parameters:
1. **Typographic Edit Distance**: Measures the number of single-character edits required to change one word into another.
2. **Phonetic Edit Distance**: Assesses the phonetic similarity between words using their encoded representations.
3. **Cosine Similarity**: Evaluates the semantic proximity of words based on their Word2Vec vectors.

By combining these metrics, the system ensures that the most relevant and likely corrections appear at the top of the suggestion list.

## Corpus Generation

A robust corpus is essential for training effective word vectors that capture the contextual nuances of the Bangla language. The corpus comprises a large and structured collection of Bangla texts sourced from diverse origins, including Wikipedia, Bangla newspapers, literature, and other online repositories. Specifically, text data is crawled from the [E-Bangla Library](https://www.ebanglalibrary.com) and the Leipzig Corpora Collection, among other sources.

The data collection process involves:
- **Web Crawling**: Utilizing Python's `requests` library to fetch webpage content.
- **Parsing**: Employing the Beautiful Soup (BS4) library to parse HTML and XML documents.
- **Sentence Segmentation**: Splitting the collected text into individual sentences to facilitate subsequent processing.

## Training the Corpus Using Word2Vec

To create meaningful word vectors that encapsulate the semantic relationships between Bangla words, the Word2Vec model is employed. This model transforms each unique word in the corpus into a dense vector of specified dimensions, capturing its contextual usage within the language.

### Preprocessing Steps

Before training, the corpus undergoes thorough preprocessing:
1. **Cleaning**: Removing all characters except Bangla alphabets to ensure uniformity.
2. **Stop-Word Removal**: Eliminating commonly used Bangla stop-words that do not contribute significant semantic value.

### Model Training

The Gensim library's `word2vec` function is used to train the model with the following configurations:
- **Vector Size**: Set to 300 dimensions, providing a balance between computational efficiency and semantic richness.
- **Window Size**: Configured to 5, meaning the model considers five words to the left and five to the right of the target word during training.
- **Training Techniques**: Both the softmax function and negative sampling are explored to optimize the model's performance.

The trained model is designed to be extensible, allowing for retraining with additional sentences as more data becomes available. This flexibility ensures that the word vectors can evolve and improve over time, maintaining their relevance and accuracy in capturing the intricacies of the Bangla language.


## Project Setup and Usage Guide

### Prerequisites
- **Git**
- **Python 3**
- **Django 1.11.2** (set up within a virtual environment)

### Steps to Run the Project

1. **Activate the Virtual Environment**
   - Navigate to the `Bangla-spell_checker` directory:
     ```bash
     cd Bangla-spell_checker
     ```
   - Activate the virtual environment:
     ```bash
     source bin/activate
     ```

2. **Run the Django Server**
   - Move to the `src` directory:
     ```bash
     cd src
     ```
   - Start the Django development server:
     ```bash
     python manage.py runserver [ip:port]
     ```
     > **Note:** The default address is `localhost:8000`.

3. **Access the Project**
   - Open your web browser and enter the IP and port you specified, or use the default (`localhost:8000`), to access the application.

### Helpful Resources

- For a tutorial on the Word2Vec model architecture, refer to this [link](http://mccormickml.com/2016/04/27/word2vec-resources/).

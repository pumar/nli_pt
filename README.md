# NLI - Portuguese
Native Language Identification of foreigner language learners of european portuguese using character level n-grams
## Introduction
The purpose of this repository is to reproduce the best algorithm/hyperparameters/feature engineering done by [this](https://www.aclweb.org/anthology/W17-5043.pdf) paper. The authors used a basic [fasttext](https://arxiv.org/pdf/1607.01759.pdf) algorithm to leverage 'good-enough' linear statistical learning algorithms as well as some deep learning with convolutions to find the optimal solution that is not resource heavy. The paper was part of a NLI competition and they ultimately received first place using decades old algorithms running against state-of-the-art deep learning solutions.

The classification task is identifying the native language of students of a foreign language by analyzing written essays using characters as tokens. In the case of the paper, that language is English. I will attempt the same algorithm on a Portuguese dataset. The feature space is expected to be larger because of diacritics.

### The Dataset
The dataset is comprised of 3,069 student essays compiled by the Center of Linguistics from the University of Lisbon. 
The students are native speakers of Chinese, English, Spanish, German, Russian, French, Japanese, Italian, Dutch, Tetum, Arabic, Polish, Korean, Romanian and Swedish. The original paper proposing this dataset can be found [here](https://www.aclweb.org/anthology/W18-0534.pdf) and the dataset itself can be downloaded from [here](http://alfclul.clul.ul.pt/crpc/NLI-PT/).

In order to fix class imbalance, only five languages were kept reducing the total number of essays to 2,477. The class distribution is as follows:

| Language      | Count         | 
| ------------- |:-------------:| 
| Spanish       | 614           | 
| Italian       | 565           |
| Mandarin      | 445           |
| German        | 438           |
| English       | 415           |

An additional preprocessing step consisted of using a token (縵, a very *infrequent* kanji) for names instead of the proposed "XXXXX" that replaced proper names in the original dataset. While fine for word level tokenization, unnecessary character repetition should be avoided when applying character level ngrams.

### The Model
The author of the paper applied a plethora of algorithms to their dataset and checked the final F1-score calculated by the competition's judges. Here, only the best overall model will be applied.

It consists of a non-parametric linear SVM applied on a bag-of-words tokenization scheme enriched with ngrams, n from 2-9. Additionally, the input is modified by a tf-idf scoring system. The term frequency was opted to be simply a binary counter (rather than a raw count), and the inverse document frequency was chosen as the regular natural logarithm of the number of documents divided by the number of documents in which the ngram appears:

idf = ln(N/n_t)

The tokenization and schematization was done using [this](https://github.com/pumar/nli_pt/blob/master/char_tokens.py) module written with efficiency in mind when dealing with character tokens.

### Results

| Maximum gram  | Weighted F1-Score (x100)|
| ------------- |:-----------------------:| 
| 1             | 39.404 ±0.951           | 
| 2             | 51.240 ±0.783           |
| 3             | 69.944 ±0.492           |

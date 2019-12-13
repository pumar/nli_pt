# NLI - Portuguese
Native Language Identification of foreigner language learners of european portuguese using character level n-grams
## Introduction
The purpose of this repository is to reproduce the best algorithm/hyperparameters/feature engineering done by [this](https://www.aclweb.org/anthology/W17-5043.pdf) paper. The authors used a basic [fasttext](https://arxiv.org/pdf/1607.01759.pdf) algorithm to leverage 'good-enough' linear statistical learning algorithms as well as some deep learning with convolutions to find the optimal solution that is not resource heavy.

The classification task is identifying the native language of students of a foreign language by analyzing written essays using characters as tokens. In the case of the paper, that language is English. I will attempt the same algorithm on a Portuguese dataset. The feature space is expected to be larger because of diacritics.

### The Dataset
The dataset is comprised of 3,069 student essays compiled by the Center of Linguistics from the University of Lisbon. 
The students are native speakers of Chinese, English, Spanish, German, Russian, French, Japanese, Italian, Dutch, Tetum, Arabic, Polish, Korean, Romanian and Swedish. The original paper proposing this dataset can be found [here](https://www.aclweb.org/anthology/W18-0534.pdf).

In order to fix class imbalance, only five languages were kept reducing the total number of essays to 2,477. The class distribution is as follows:

| Language      | Count         | 
| ------------- |:-------------:| 
| Spanish       | 614           | 
| Italian       | 565           |
| Mandarin      | 445           |
| German        | 438           |
| English       | 415           |


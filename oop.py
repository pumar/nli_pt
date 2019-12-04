# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:03:16 2019

@author: z5g1327
"""

import os

class NGramTokenizer(object):
    """
    
    """
    def __init__(self, ngrams=1,
                 skipgram=1,
                 **kwargs):
        
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        
        self.ngrams = ngrams
        self.skipgram = skipgram
        self.ngram_index = dict()
        
    def text_fitting(self,corpus,one_char=False):
        """This function should receive as input the entire available corpus\
           so as to provice a representative relative importance of ngrams
           RETURNS: a dictionary mapping ngrams to ordered integers
        """
        
        for gram in range(1,self.ngrams+1):
            for document in corpus:
                if gram == 1:
                    skip = 1
                else:
                    skip = self.skipgram
                for char_index in range(0,len(document)-gram+1,skip):
                    current_gram = document[char_index:char_index+gram]
                    if current_gram in self.ngram_index:
                        self.ngram_index[current_gram] += 1
                    else:
                        self.ngram_index[current_gram] = 1
        # Filters characters that only appear once in corpus
        #if one_char:
        #    continue
        dict_list= list()
        ### Sorting the dictionary through a 'zipped' list
        for (key,value) in self.ngram_index.items():
            dict_list.append((key,value))
        dict_list = sorted(dict_list,key=lambda x: x[1],reverse=True)
        ### Refactors the dictionary with each value now corresponding to the order\
        #\  in which it is prevalent in the corpus. (e.g. space-> ' ' = 1)\
        ### OBS: Starts from 1, since 0 is a reserved value for padding sequences
        for i,pair in enumerate(dict_list):
            self.ngram_index[pair[0]]=i+1

    def bag_of_words(self,corpus):
    
        bow = list()
        ngram=max([len(gram) for gram in self.ngram_index.keys()])
        for document in corpus:
            doc_gram = [0]*len(self.ngram_index)
            for gram in range(1,ngram+1):
                if gram == 1:
                    skip = 1
                else:
                    skip = self.skipgram
                for char_index in range(0,len(document)-gram+1,skip):
                    current_gram = document[char_index:char_index+gram]
                    print(current_gram)
                    if current_gram in self.ngram_index.keys():
                        doc_gram[self.ngram_index[current_gram]-1] += 1
            bow.append(doc_gram)
        return bow

def text_file_opener(file_name):
    with open(os.getcwd() + file_name,'r',encoding='utf-8') as f:
        return f.read().replace('\n',' ')

tokenizer = NGramTokenizer(15,2)
texts = [text_file_opener(r'\teste.txt'),text_file_opener(r'\teste2.txt')]
tokenizer.text_fitting(texts)

BoW = tokenizer.bag_of_words(texts)

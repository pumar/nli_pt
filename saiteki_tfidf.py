# -*- coding: utf-8 -*-

from numpy import multiply, log
import numpy as np

class NGramTokenizer(object):
    """
    Character-level tokenizer class that efficiently includes ngrams into the 
    output bag of words model, which can be optionally incremented with tf-idf. 
    Alternatively, also includes the option to build sequential models for 
    neural networks with convolution layer(s).
    
    INPUT:
       
        >> ngrams: the maximum size of the ngrams created. For example, a
        ngram = 5 will create a regular bow model and increment it with ngrams
        with size 2,3,4 and 5.
        >> gramskip: In order to reduce the feature space (it gets huge with 
        bigger ngrams), it is useful to pass small integers to this parameter.
        The integer is used to determine how many character should be skipped
        when calculating the next ngram. In general, it is better to keep it
        at 1 if you have enough memory.
        >> min_count: the minimum number of times ngrams (1 to n) must appear
        in the first layer (bow or sequence). Any number less than min_count
        will be filtered out, thus reducing the feature space and sparsity.
        
    """
    def __init__(self, ngrams=1,
                 gramskip=1,
                 min_count=1,
                 **kwargs):
        
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        
        if gramskip != 1:
            raise ValueError('gramskip must be 1.')
            
        self.ngrams = ngrams
        self.gramskip = gramskip
        self.min_count = min_count
        self.ngram_dict = dict()
        
    def text_fitting(self,
                     corpus,
                     **kwargs):
        
        """This function should receive as input the entire available corpus\
           so as to provice a representative relative importance of ngrams
           RETURNS: a dictionary mapping ngrams to ordered integers
        """
        
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        
        for gram in range(1,self.ngrams+1):
            for document in corpus:
                if gram == 1:
                    skip = 1
                else:
                    skip = self.gramskip
                for char_index in range(0,len(document)-gram+1,skip):
                    current_gram = document[char_index:char_index+gram]
                    if current_gram in self.ngram_dict:
                        self.ngram_dict[current_gram] += 1
                    else:
                        self.ngram_dict[current_gram] = 1
                
        # Filters characters that appear infrequently
        if self.min_count > 1:
            temp_dict = {}
            for key in self.ngram_dict.keys():
                if self.ngram_dict[key] >= self.min_count:
                    temp_dict[key] = self.ngram_dict[key]
            self.ngram_dict = temp_dict
        
        
        dict_list= list()
        
        ### Sorting the dictionary through a 'zipped' list
        for (key,value) in self.ngram_dict.items():
            dict_list.append((key,value))
            
        dict_list = sorted(dict_list,key=lambda x: x[1],reverse=True)
        """
        Refactors the dictionary with each value now corresponding to the order
        in which it is prevalent in the corpus. (e.g. space-> ' ' = 1)\
        OBS: Starts from 1, since 0 is a reserved value for padding when
        using sequences
        """
        for i,pair in enumerate(dict_list):
            self.ngram_dict[pair[0]]=i+1

    def bag_of_words(self,
                     corpus,
                     **kwargs):
        
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        
        bow = list()
        
        for document in corpus:
            doc_gram = [0]*len(self.ngram_dict)
            for gram in range(1,self.ngrams+1):
                if gram == 1:
                    skip = 1
                else:
                    skip = self.gramskip
                for char_index in range(0,len(document)-gram+1,skip):
                    current_gram = document[char_index:char_index+gram]
                    if current_gram in self.ngram_dict.keys():
                        doc_gram[self.ngram_dict[current_gram]-1] += 1
            bow.append(doc_gram)
            
        return np.array(bow)
    
    def tf_idf(self,
               corpus,
               **kwargs):
        """
        tf-idf weights applied to a bag of words model.
        INPUTS:
            >> corpus: a list of documents.
            >> tf_weighting:  term frequency weighting schemes.
            (Implemented: binary)
            >> idf_weighting: inverse document frequency weighting scheme.
            (Implemented: idf)
        """
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        

        if self.gramskip != 1:
            print("WARNING: 'gramskip' values different than 1 are ill-advised\
                  for a tf-idf model. \n")

        tfs = self.bag_of_words(corpus)

        
        
        tfs = np.where(tfs == 0, 0, 1)
    
        return multiply(tfs,log(len(corpus)/np.sum(tfs,axis=0)))
        

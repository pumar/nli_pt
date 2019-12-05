# -*- coding: utf-8 -*-


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
        self.ngram_dict = dict()
        
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
                    if current_gram in self.ngram_dict:
                        self.ngram_dict[current_gram] += 1
                    else:
                        self.ngram_dict[current_gram] = 1
        # Filters characters that only appear once in corpus
        #if one_char:
        #    continue
        dict_list= list()
        ### Sorting the dictionary through a 'zipped' list
        for (key,value) in self.ngram_dict.items():
            dict_list.append((key,value))
        dict_list = sorted(dict_list,key=lambda x: x[1],reverse=True)
        ### Refactors the dictionary with each value now corresponding to the order\
        #\  in which it is prevalent in the corpus. (e.g. space-> ' ' = 1)\
        ### OBS: Starts from 1, since 0 is a reserved value for padding sequences
        for i,pair in enumerate(dict_list):
            self.ngram_dict[pair[0]]=i+1

    def bag_of_words(self,corpus):
    
        bow = list()
        ngram=max([len(gram) for gram in self.ngram_dict.keys()])
        for document in corpus:
            doc_gram = [0]*len(self.ngram_dict)
            for gram in range(1,ngram+1):
                if gram == 1:
                    skip = 1
                else:
                    skip = self.skipgram
                for char_index in range(0,len(document)-gram+1,skip):
                    current_gram = document[char_index:char_index+gram]
                    if current_gram in self.ngram_dict.keys():
                        doc_gram[self.ngram_dict[current_gram]-1] += 1
            bow.append(doc_gram)
        return bow

    def ngram_index(self):
        
        if not self.ngram_dict:
            raise Exception("No available index. Please fit corpus with method text_fitting.")
            
        for key in self.ngram_dict.keys():
            self.ngram_dict[key] -= 1
        return self.ngram_dict
        
        


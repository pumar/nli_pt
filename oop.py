# -*- coding: utf-8 -*-


class NGramTokenizer(object):
    """
    Character-level tokenizer class that efficiently includes ngrams into the 
    output bag of words model. Alternatively, also includes the option to build
    sequential models for neural networks with convolution layer(s).
    
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
        
        if gramskip < 1:
            raise ValueError('gramskip must be bigger than 0.')
            
        self.ngrams = ngrams
        self.gramskip = gramskip
        self.min_count = min_count
        self.ngram_dict = dict()
        
    def text_fitting(self,corpus):
        
        """This function should receive as input the entire available corpus\
           so as to provice a representative relative importance of ngrams
           RETURNS: a dictionary mapping ngrams to ordered integers
        """
        
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
                     corpus):
    
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
            
        return bow
    
    def to_sequence(self,
                    corpus,
                    max_size=None):
        """
        Turns each document in a sequence of integers with length $NUMBER
        OF CHARACTERS$ that is equal to an ordered list with the most frequent
        character having the value 1.
        
        INPUT:
            >> corpus: a list of documents
            >> max_size: the maximum number of allowed characters per document.
            If there are more characters in a document the remaining characters
            will not be included. If there are less characters, the sequence 
            will be padded with zeros. The default value is the largest document
            in the corpus.
        """
        if self.ngrams != 1 or self.gramskip != 1:
            raise ValueError("'ngrams' AND 'gramskip' values must be 1 for a sequencer model.")
        
        if not max_size:
            max_size = max([len(doc) for doc in corpus])
            
        sequence = list()
        
        for document in corpus:
            doc_chars = []
            for character in document:
                if character in self.ngram_dict.keys():
                    doc_chars.append(self.ngram_dict[character])
            ### Sequence padding/limiting
            if len(doc_chars) < max_size:
                doc_chars.extend([0]*(max_size - len(doc_chars)))
            elif len(doc_chars) > max_size:
                doc_chars = doc_chars[:max_size]
                
            sequence.append(doc_chars)
        
        return sequence
        
    def sequence_to_text(self,
                         sequence):
        """
        Function that returns a text from a sequence or list of sequences.
        ATT: if min_count > 1, some of the original sequences may be incomplete
        OUTPUT:
            >> A string built using the character index
        """    
        
        if self.ngrams != 1 or self.gramskip != 1:
            raise ValueError("'ngrams' AND 'gramskip' values must be 1 for a sequencer model.")
        
        ### If list of lists,　flatten into a 1D list
        if type(sequence[0]) == list:
            sequence = [item for sublist in sequence for item in sublist]
        
        if self.min_count > 1:
            print("Warning: min_count was set as {}. Some characters might be omitted in the string returned by this function. \n".format(str(self.min_count)))
        
        output_text = list()
        
        #Invert dictionary for mapping
        invert_dict = {v: k for k, v in self.ngram_dict.items()}
        
        for char_index in sequence:
            if char_index in invert_dict.keys():
                output_text.append(invert_dict[char_index])
                
        return "".join(output_text)
        
    
    def ngram_index(self):
        
        if not self.ngram_dict:
            raise Exception("No available index. Please fit corpus with method text_fitting.")
            
        for key in self.ngram_dict.keys():
            self.ngram_dict[key] -= 1
            
        return self.ngram_dict
        
       

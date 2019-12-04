# -*- coding: utf-8 -*-

import os


def text_file_opener(file_name):
    with open(os.getcwd() + file_name,'r',encoding='utf-8') as f:
        return f.read().replace('\n',' ')
#GLOBALS (will go inside class initialization)
texts = [text_file_opener(r'\teste.txt'),text_file_opener(r'\teste2.txt')]
ngrams = 1
skipgram = 1
### Fix funciton input: From already concatenated text to a list of documents.
def fit_to_text(corpus,ngram=ngrams,char_skip=skipgram,one_char=False):
    """This function should receive as input the entire available corpus\
       so as to provice a representative relative importance of characters
       RETURNS: a dictionary mapping ngrams to ordered integers
    """
    #token_dict = {}
    """ Populates a dictionary with each key,value pair corresponding to a \
      character and a count of its presence in the corpus.
    """
    if type(corpus) == str:
        corpus = [corpus]
    ngram_dict = {}
    for gram in range(1,ngram+1):
        for document in corpus:
            for char_index in range(0,len(document)-gram+1,char_skip):
                current_gram = document[char_index:char_index+gram]
                if current_gram in ngram_dict:
                    ngram_dict[current_gram] += 1
                else:
                    ngram_dict[current_gram] = 1
    # Filters characters that only appear once in corpus
    if one_char:
        ngram_dict = dict_filter(ngram_dict)
    dict_list= list()
    ### Sorting the dictionary through a 'zipped' list
    for (key,value) in ngram_dict.items():
        dict_list.append((key,value))
    dict_list = sorted(dict_list,key=lambda x: x[1],reverse=True)
    ### Refactors the dictionary with each value now corresponding to the order\
    #\  in which it is prevalent in the corpus. (e.g. space-> ' ' = 1)\
    ### OBS: Starts from 1, since 0 is a reserved value for padding sequences
    for i,pair in enumerate(dict_list):
        ngram_dict[pair[0]]=i+1
    return ngram_dict
    """
    for character in text:
        if character in token_dict.keys():
            token_dict[character] += 1
        else:
            token_dict[character] = 1
    
    # Filters characters that only appear once in corpus
    if one_char:
        token_dict = dict_filter(token_dict)
    dict_list= list()
    ### Sorting the dictionary through a 'zipped' list
    for (key,value) in token_dict.items():
        dict_list.append((key,value))
    dict_list = sorted(dict_list,key=lambda x: x[1],reverse=True)
    ### Refactors the dictionary with each value now corresponding to the order\
    #\  in which it is prevalent in the corpus. (e.g. space-> ' ' = 1)\
    ### OBS: Starts from 1, since 0 is a reserved value for padding sequences
    for i,pair in enumerate(dict_list):
        token_dict[pair[0]]=i+1
    return token_dict
    """

def sequencer(corpus,cmap):
    ### Turns each document into a sequence of integers.
    ### Each integer is part of a sequence from 1 to $NUMBER_OF_CHARACTERS
    if type(corpus) == str:
        corpus = [corpus]
    sequence = list()
    for document in corpus:
        doc_chars = []
        for character in document:
            if character in cmap.keys():
                doc_chars.append(cmap[character])
        sequence.append(doc_chars)
    return sequence


def bag_of_words(corpus,gmap):
    if type(corpus) == str:
        corpus = [corpus]
    bow = list()
    ngram=max([len(gram) for gram in gmap.keys()])
    for document in corpus:
        doc_gram = [0]*len(gmap)
        for gram in range(1,ngram+1):                   
            for char_index in range(0,len(document)-gram+1,skipgram):
                current_gram = document[char_index:char_index+gram]
                if current_gram in gmap.keys():
                    doc_gram[gmap[current_gram]-1] += 1
        bow.append(doc_gram)
    return bow
            
    

def dict_filter(dictObj):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item appears in the text more than once
        if dictObj[key] != 1:
            newDict[key] = value
    return newDict



character_map = fit_to_text(texts,9)
#sequence = sequencer(texts,character_map)
BoW = bag_of_words(texts,character_map)
#ngram_bow = append_ngram(texts,BoW,2,1)

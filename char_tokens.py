# -*- coding: utf-8 -*-

import os


def fit_to_text(text):
    """This function should receive as input the entire available corpus\
       so as to provice a representative relative importance of characters
       RETURNS: a dictionary mapping characters to ordered integers
    """
    token_dict = {}
    """ Populates a dictionary with each key,value pair corresponding to a \
      character and a count of its presence in the corpus.
    """
    for character in text:
        if character in token_dict.keys():
            token_dict[character] += 1
        else:
            token_dict[character] = 1
    # Filters characters that only appear once in corpus
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


def bag_of_words(corpus,cmap):
    if type(corpus) == str:
        corpus = [corpus]
    bow = list()
    for document in corpus:
        doc_chars = [0]*len(cmap)
        for character in document:
            if character in cmap.keys():
                doc_chars[cmap[character]-1] += 1
        bow.append(doc_chars)
        return bow

def append_ngram(corpus,bow,ngram=1,char_skip=1):
    if ngram==1:
        return bow
    for gram in range(1,ngrams+2):
        for document in corpus:
            for char_index in range(0,len(document)-ngram,char_skip):
            
    

def dict_filter(dictObj):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item appears in the text more than once
        if dictObj[key] != 1:
            newDict[key] = value
    return newDict


def text_file_opener(file_name):
    with open(os.getcwd() + file_name,'r',encoding='utf-8') as f:
        return f.read().replace('\n',' ')
    
texts = text_file_opener(r'\teste.txt')
character_map = fit_to_text(texts)
sequence = sequencer(texts,character_map)
BoW = bag_of_words(texts,character_map)
ngram_bow = append_ngram(texts,BoW,2,1)

#print(len(append_ngram(sequence)[0]),len(append_ngram(sequence,2,1)[0]),len(append_ngram(sequence,2,2)[0]))

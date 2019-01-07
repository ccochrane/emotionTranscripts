#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 05:38:46 2019

@author: chriscochrane
"""

import re

import pandas as pd
import nltk
import os
import numpy as np
import sys
from nltk.corpus import stopwords
import time

import gensim

from gensim.models import Word2Vec
from gensim.models import word2vec
from gensim.models import Phrases
import logging


tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

stopwords = stopwords.words('english')


hansardSpeeches = pd.read_csv('hansardExtractedSpeechesFull.csv', sep="\t", encoding="utf-8", header=0) 



print(hansardSpeeches['mentionedEntityName'][1])

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]','', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

def hansard_to_sentences(hansard, tokenizer, remove_stopwords=False ):
    #print("currently processing: word tokenizer")
    start_time = time.time()
    try:
        # 1. Use the NLTK tokenizer to split the text into sentences
        raw_sentences = tokenizer.tokenize(hansard.strip())
        # 2. Loop over each sentence
        sentences = []
        for raw_sentence in raw_sentences:
            # If a sentence is empty, skip it
            if len(raw_sentence) > 0:
                # Otherwise, call sentence_to_wordlist to get a list of words
                sentences.append(sentence_to_wordlist(raw_sentence))
        # 3. Return the list of sentences (each sentence is a list of words, so this returns a list of lists)
        len(sentences)
        return sentences
    except:
        print('nope')

    end_time = time.time()-start_time

questions = hansardSpeeches['speech']

questions = pd.Series.tolist(questions)
sentences = []

for i in range(0,len(questions)):

    start_time = time.time()

    try:
        # Need to first change "./." to "." so that sentences parse correctly
        hansard = questions[i].replace("/.", '')
        # Now apply functions
        sentences += hansard_to_sentences(hansard, tokenizer)
    except:
        print('no!')

print("There are " + str(len(sentences)) + " sentences in our corpus of questions.")

print("currently processing: training model")
start_time = time.time()



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

num_features = 300    # Word vector dimensionality
min_word_count = 10   # Minimum word count 
num_workers = 4       # Number of threads to run in parallel
context = 6           # Context window size
downsampling = 1e-3   # Downsample setting for frequent words

model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

model.init_sims(replace=True)

model_name = 'hansardQuestions'
model.save(model_name)
new_model = gensim.models.Word2Vec.load('hansardQuestions')

vocab = list(model.wv.vocab.keys())


print("Process complete--the first 25 words in the vocabulary are:")

print(vocab[:25])

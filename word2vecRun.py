# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 14:54:42 2019

@author: chris
"""

import gensim
import numpy as np
from operator import itemgetter
import pylab as pl
import scipy.stats as stats
import nltk
import time
import pandas as pd
import re
from nltk.corpus import stopwords


model = gensim.models.Word2Vec.load('hansardQuestions')


good = model['good']
excellent = model['excellent']
correct = model['correct']
best = model['best']
happy = model['happy']
great = model['great']
positive = model['positive']
fortunate = model['fortunate']


bad = model['bad']
terrible = model['terrible']
wrong = model['wrong']
worst = model['worst']
disappointed = model['disappointed']
negative = model['negative']
unfortunate = model['unfortunate']

vocab = list(model.wv.vocab.keys())

vocab100 = vocab[:40597]


runningTally=[]
dictOfWeights = {}


for word in vocab100:

    word_model = model[word]

    pos1 = np.dot(word_model, good) / (np.linalg.norm(word_model) * np.linalg.norm(good))
    pos2 = np.dot(word_model, excellent) / (np.linalg.norm(word_model) * np.linalg.norm(excellent))
    pos3 = np.dot(word_model, correct) / (np.linalg.norm(word_model) * np.linalg.norm(correct))
    pos4 = np.dot(word_model, best) / (np.linalg.norm(word_model) * np.linalg.norm(best))
    pos5 = np.dot(word_model, happy) / (np.linalg.norm(word_model) * np.linalg.norm(happy))
    pos6 = np.dot(word_model, positive) / (np.linalg.norm(word_model) * np.linalg.norm(positive))
    pos7 = np.dot(word_model, fortunate) / (np.linalg.norm(word_model) * np.linalg.norm(fortunate))

    neg1 = np.dot(word_model, bad) / (np.linalg.norm(word_model) * np.linalg.norm(bad))
    neg2 = np.dot(word_model, terrible) / (np.linalg.norm(word_model) * np.linalg.norm(terrible))
    neg3 = np.dot(word_model, wrong) / (np.linalg.norm(word_model) * np.linalg.norm(wrong))
    neg4 = np.dot(word_model, worst) / (np.linalg.norm(word_model) * np.linalg.norm(worst))
    neg5 = np.dot(word_model, disappointed) / (np.linalg.norm(word_model) * np.linalg.norm(disappointed))
    neg6 = np.dot(word_model, negative) / (np.linalg.norm(word_model) * np.linalg.norm(negative))
    neg7 = np.dot(word_model, unfortunate) / (np.linalg.norm(word_model) * np.linalg.norm(unfortunate))

    pos = sum([pos1, pos2, pos3, pos4,  pos5, pos6, pos7])/7
    neg = sum([neg1, neg2, neg3, neg4, neg5, neg6, neg7])/7
    posneg = pos-neg
    result = (word, posneg)
    runningTally.append(result)
    dictOfWeights[word] = result


runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))


vocab_obj_good = model.wv.vocab["good"]
print("good", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["excellent"]
print("excellent", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["correct"]
print("correct", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["best"]
print("best", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["happy"]
print("happy", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["happy"]
print("great", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["positive"]
print("positive", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["fortunate"]
print("fortunate", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["bad"]
print("bad", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["terrible"]
print("terrible", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["wrong"]
print("wrong", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["worst"]
print("worst", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["disappointed"]
print("disappointed", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["negative"]
print("negative", vocab_obj_good.count)

vocab_obj_good = model.wv.vocab["unfortunate"]
print("unfortunate", vocab_obj_good.count)



stopwords = stopwords.words('english')
sentence = "Mr. Speaker, the objective of the Government of Canada is to surveil them and contain them to ensure that they do not harm more people, and indeed bring the full force of Canadian justice against them for fighting for a terrorist organization."
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
raw_sentences = tokenizer.tokenize(sentence.strip())

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    #start_time = time.time()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

#Import Data


hansardVideos = pd.read_csv("hansardExtractedVideoTranscripts.csv", encoding='utf-8')

df = pd.DataFrame(columns=['Label', 'Date' 'ID_main', 'youTube',
                  'timeStamp', 'Speaker', 'French', 'Party',
                  'Seconds', 'English', 'Floor', 
                  'Sentiment', 'sentencePolarity',
                  'wordPolaritySummed', 'sentencePolaritySTD',
                  'countedWords'])


labelList = []
dateList = []
IDmainList = []
youTubeList = []
timeStampList = []
speakerList = []
frenchList = []
partyList = []
secondsList = []
englishList = []
floorList = []
sentenceList = []
sentimentList = []
wordPolaritySummedList = []
sentencePolarityList = []
sentencePolaritySTDList = []
countedWordsList = []
    
    
i = 0
for x in range(0, len(hansardVideos["Label"])):
    labelList.append(hansardVideos["Label"][i])
    dateList.append(hansardVideos["Date"][i])
    IDmainList.append(hansardVideos["ID_main"][i])
    youTubeList.append(hansardVideos["youTube"][i])
    timeStampList.append(hansardVideos["timeStamp"][i])
    speakerList.append(hansardVideos["Speaker"][i])
    frenchList.append(hansardVideos["French"][i])
    partyList.append(hansardVideos["party"][i])
    secondsList.append(hansardVideos["seconds"][i])
    englishList.append(hansardVideos["english"][i])
    floorList.append(hansardVideos["floor"][i])

    sentenceList.append(hansardVideos["english"][i])
    sentence = hansardVideos["english"][i]
    sentence_words = sentence_to_wordlist(sentence)
    sentiment = 0
    sentencePolarity = 0
    wordPolaritySummed = 0
    sentencePolaritySTD = 0
    countedWords = 0
    
    for word in sentence_words:

        try:

            word_model = model[word]

            pos1 = np.dot(word_model, good) / (np.linalg.norm(word_model) * np.linalg.norm(good))
            pos2 = np.dot(word_model, excellent) / (np.linalg.norm(word_model) * np.linalg.norm(excellent))
            pos3 = np.dot(word_model, correct) / (np.linalg.norm(word_model) * np.linalg.norm(correct))
            pos4 = np.dot(word_model, best) / (np.linalg.norm(word_model) * np.linalg.norm(best))
            pos5 = np.dot(word_model, happy) / (np.linalg.norm(word_model) * np.linalg.norm(happy))
            pos6 = np.dot(word_model, positive) / (np.linalg.norm(word_model) * np.linalg.norm(positive))
            pos7 = np.dot(word_model, fortunate) / (np.linalg.norm(word_model) * np.linalg.norm(fortunate))

            neg1 = np.dot(word_model, bad) / (np.linalg.norm(word_model) * np.linalg.norm(bad))
            neg2 = np.dot(word_model, terrible) / (np.linalg.norm(word_model) * np.linalg.norm(terrible))
            neg3 = np.dot(word_model, wrong) / (np.linalg.norm(word_model) * np.linalg.norm(wrong))
            neg4 = np.dot(word_model, worst) / (np.linalg.norm(word_model) * np.linalg.norm(worst))
            neg5 = np.dot(word_model, disappointed) / (np.linalg.norm(word_model) * np.linalg.norm(disappointed))
            neg6 = np.dot(word_model, negative) / (np.linalg.norm(word_model) * np.linalg.norm(negative))
            neg7 = np.dot(word_model, unfortunate) / (np.linalg.norm(word_model) * np.linalg.norm(unfortunate))

            pos = sum([pos1, pos2, pos3, pos4, pos5, pos6, pos7]) / 7
            neg = sum([neg1, neg2, neg3, neg4, neg5, neg6, neg7]) / 7
            posneg = pos - neg
            sentiment += posneg
            wordPolaritySummed += abs(posneg)
            countedWords +=1
            

        except:
            
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    if countedWords>0:
        sentencePolaritySTD = abs(sentiment)/countedWords
    else:
        sentencePolaritySTD = np.NaN
    
    
    sentencePolaritySTDList.append(sentencePolaritySTD)
    
    i+=1
    
w2vScores = pd.DataFrame({'label': labelList, 
                               'date': dateList, 
                               'IDMain': IDmainList, 
                               'youTube': youTubeList, 
                               'timeStamp': timeStampList, 
                               'speaker': speakerList,
                               'french': frenchList, 
                               'party': partyList,
                               'seconds': secondsList,
                               'english': englishList,
                               'floor': floorList,
                               'sentiment': sentimentList,
                               'sentencePolarity': sentencePolarityList,
                               'wordPolaritySummed': wordPolaritySummedList,
                               'sentencePolaritySTD': sentencePolaritySTDList,
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vScores.csv", sep='\t', encoding='utf-8')





# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 14:54:42 2019

@author: chris cochrane

NOTES: Requires Windows. Comparing w2vec Models
"""

#-----------------------------------------------------------------------------
# Initialization
#-----------------------------------------------------------------------------


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




#-----------------------------------------------------------------------------
# Loading stored w2v Model
#-----------------------------------------------------------------------------


model1 = gensim.models.Word2Vec.load('hansardQuestions')

#https://drive.google.com/uc?id=0B7XkCwpI5KDYNlNUTTlSS21pQmM&export=download
model2 = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  



#-----------------------------------------------------------------------------
# Analogies (Hansard vs Google News)
#-----------------------------------------------------------------------------




model1.wv.most_similar(positive=['toronto', 'alberta'], negative=['ontario'])
model2.wv.most_similar(positive=['Toronto', 'Alberta'], negative=['Ontario'])


model1.wv.most_similar(positive=['washington', 'france'], negative=['usa'])
model2.wv.most_similar(positive=['Washington', 'France'], negative=['USA'])

model1.wv.most_similar(positive=['washington', 'canada'], negative=['usa'])
model2.wv.most_similar(positive=['Washington', 'Canada'], negative=['USA'])

model1.wv.most_similar(positive=['king', 'woman'], negative=['man'])
model2.wv.most_similar(positive=['king', 'woman'], negative=['man'])

model1.wv.most_similar(positive=['hatred', 'immigrants'])
model2.wv.most_similar(positive=['hatred', 'immigrants'])

model1.wv.most_similar(positive=['hockey', 'ball'], negative=['puck'])
model2.wv.most_similar(positive=['hockey','ball'], negative=['puck'])


model1.wv.most_similar(positive=['war', 'evil'], negative=['bravery'])
model2.wv.most_similar(positive=['war', 'evil'], negative=['bravery'])

model1.wv.most_similar(positive=['war', 'bravery'], negative=['evil'])
model2.wv.most_similar(positive=['war', 'bravery'], negative=['evil'])

model1.wv.most_similar(positive=['israel', 'muslim'], negative=['jewish'])
model2.wv.most_similar(positive=['Israel', 'muslim'], negative=['jewish'])

model1.wv.most_similar(positive=['tokyo', 'china'], negative=['japan'])
model2.wv.most_similar(positive=['Tokyo', 'China'], negative=['Japan'])

model1.wv.most_similar(positive=['fish', 'prairies'], negative=['ocean'])
model2.wv.most_similar(positive=['fish', 'prairies'], negative=['ocean'])

model1.wv.most_similar(positive=['harvard', 'canadian'], negative=['american'])
model2.wv.most_similar(positive=['Harvard', 'Canadian'], negative=['American'])


##############################################################################
#-----------------------------------------------------------------------------
# Replicating Sentiment Analysis on Google News
#-----------------------------------------------------------------------------
##############################################################################



#-----------------------------------------------------------------------------
# Seed Words (Adapted from Turney and Littman)
#-----------------------------------------------------------------------------

good = model2['good']
excellent = model2['excellent']
correct = model2['correct']
best = model2['best']
happy = model2['happy']
positive = model2['positive']
fortunate = model2['fortunate']


bad = model2['bad']
terrible = model2['terrible']
wrong = model2['wrong']
worst = model2['worst']
disappointed = model2['disappointed']
negative = model2['negative']
unfortunate = model2['unfortunate']

vocab = list(model2.wv.vocab.keys()) #the full vocabulary of Google News


# an empty list for storing wights and an empty dictionary for linking
# weights and words

runningTally=[]
dictOfWeights = {}

#-----------------------------------------------------------------------------
# Model
#-----------------------------------------------------------------------------

'''for every word in the google news corpus, calculate its cosine similarity to the 
lists of positive words and negative words, then substract the sum of that
word's cosine simlarity to negative seed words from its cosine similarity to the
postive seed words.''' 

for word in vocab:

    word_model = model2[word]

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



#-----------------------------------------------------------------------------
# Results
#-----------------------------------------------------------------------------

'''The 100 most positive signed and most negative signed words'''

runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))


'''word counts for the seed words'''
vocab_obj_good = model2.wv.vocab["good"]
print("good", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["excellent"]
print("excellent", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["correct"]
print("correct", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["best"]
print("best", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["happy"]
print("happy", vocab_obj_good.count)


vocab_obj_good = model2.wv.vocab["positive"]
print("positive", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["fortunate"]
print("fortunate", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["bad"]
print("bad", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["terrible"]
print("terrible", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["wrong"]
print("wrong", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["worst"]
print("worst", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["disappointed"]
print("disappointed", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["negative"]
print("negative", vocab_obj_good.count)

vocab_obj_good = model2.wv.vocab["unfortunate"]
print("unfortunate", vocab_obj_good.count)


#-----------------------------------------------------------------------------
# Apply Lexicon
#-----------------------------------------------------------------------------

'''Apply the Lexicon to score the transcripts of the video clips.'''

#remove stopwords.  They are not relevant to sentiment scoring.

stopwords = stopwords.words('english')

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

#Import Data re: transcripts of video snippets

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
hansardVideos = pd.read_csv(gitHub, encoding='utf-8')

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
countedWordsList = []
    

'''A loop for cycling through the list of rows in the hansardVideo
Transcripts.'''
    
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
    '''break the sentence into words'''
    sentence_words = sentence_to_wordlist(sentence)
    '''initialize variables'''
    sentiment = 0 #positivity minus negativity
    sentencePolarity = 0 #absolute values of positivity minus negativity
    wordPolaritySummed = 0 #sum of absolute value of word polarities
    countedWords = 0
    
    '''for every word in the sentence, subtract the sum of its cosine 
    similarity to the negative seed words from the sum of its cosine
    similarity to the positive seed words, and then sum the difference
    across all words in the sentence.'''
    
    for word in sentence_words:

        try:

            word_model = model2[word]

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
            
            #handful of garbage words -- did not meet minimum word threschold
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    
    i+=1


'''output to csv file'''
    
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
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vScoresGoogleNews.csv", sep=',', encoding='utf-8')


#


##############################################################################
#-----------------------------------------------------------------------------
# Replicating Sentiment Analysis with Excellent/Terrible
#-----------------------------------------------------------------------------
##############################################################################




#-----------------------------------------------------------------------------
# Seed Words (Adapted from Turney and Littman)
#-----------------------------------------------------------------------------

excellent = model1['excellent']

terrible = model1['terrible']


vocab = list(model1.wv.vocab.keys()) #the full vocabulary of Google News


# an empty list for storing wights and an empty dictionary for linking
# weights and words

runningTally=[]
dictOfWeights = {}

#-----------------------------------------------------------------------------
# Model
#-----------------------------------------------------------------------------

'''for every word in the hansard, calculate its cosine similarity to the 
lists of positive words and negative words, then substract the sum of that
word's cosine simlarity to negative seed words from its cosine similarity to the
postive seed words.''' 

for word in vocab:

    word_model = model1[word]

    pos1 = np.dot(word_model, excellent) / (np.linalg.norm(word_model) * np.linalg.norm(excellent))


    neg1 = np.dot(word_model, terrible) / (np.linalg.norm(word_model) * np.linalg.norm(terrible))


    pos = sum([pos1])
    neg = sum([neg1])
    posneg = pos-neg
    result = (word, posneg)
    runningTally.append(result)
    dictOfWeights[word] = result



#-----------------------------------------------------------------------------
# Results
#-----------------------------------------------------------------------------

'''The 100 most positive signed and most negative signed words'''

runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))

#-----------------------------------------------------------------------------
# Apply Lexicon
#-----------------------------------------------------------------------------

'''Apply the Lexicon to score the transcripts of the video clips.'''

#remove stopwords.  They are not relevant to sentiment scoring.
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

#Import Data re: transcripts of video snippets

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
hansardVideos = pd.read_csv(gitHub, encoding='utf-8')

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
countedWordsList = []
    

'''A loop for cycling through the list of rows in the hansardVideo
Transcripts.'''
    
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
    '''break the sentence into words'''
    sentence_words = sentence_to_wordlist(sentence)
    '''initialize variables'''
    sentiment = 0 #positivity minus negativity
    sentencePolarity = 0 #absolute values of positivity minus negativity
    wordPolaritySummed = 0 #sum of absolute value of word polarities
    countedWords = 0
    
    '''for every word in the sentence, subtract the sum of its cosine 
    similarity to the negative seed words from the sum of its cosine
    similarity to the positive seed words, and then sum the difference
    across all words in the sentence.'''
    
    for word in sentence_words:

        try:

            word_model = model1[word]

            pos1 = np.dot(word_model, excellent) / (np.linalg.norm(word_model) * np.linalg.norm(excellent))

            neg1 = np.dot(word_model, terrible) / (np.linalg.norm(word_model) * np.linalg.norm(terrible))


            pos = sum([pos1]) 
            neg = sum([neg1]) 
            posneg = pos - neg
            sentiment += posneg
            wordPolaritySummed += abs(posneg)
            countedWords +=1
            

        except:
            
            #handful of garbage words -- did not meet minimum word threschold
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    
    i+=1


'''output to csv file'''
    
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
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vExcellentTerribleOnly.csv", sep=',', encoding='utf-8')


##############################################################################
#-----------------------------------------------------------------------------
# Replicating Sentiment Analysis with Correct/Wrong
#-----------------------------------------------------------------------------
##############################################################################




#-----------------------------------------------------------------------------
# Seed Words (Adapted from Turney and Littman)
#-----------------------------------------------------------------------------

correct = model1['correct']

wrong = model1['wrong']


vocab = list(model1.wv.vocab.keys()) #the full vocabulary of Google News


# an empty list for storing wights and an empty dictionary for linking
# weights and words

runningTally=[]
dictOfWeights = {}

#-----------------------------------------------------------------------------
# Model
#-----------------------------------------------------------------------------

'''for every word in the hansard, calculate its cosine similarity to the 
lists of positive words and negative words, then substract the sum of that
word's cosine simlarity to negative seed words from its cosine similarity to the
postive seed words.''' 

for word in vocab:

    word_model = model1[word]

    pos1 = np.dot(word_model, correct) / (np.linalg.norm(word_model) * np.linalg.norm(correct))


    neg1 = np.dot(word_model, wrong) / (np.linalg.norm(word_model) * np.linalg.norm(wrong))


    pos = sum([pos1])
    neg = sum([neg1])
    posneg = pos-neg
    result = (word, posneg)
    runningTally.append(result)
    dictOfWeights[word] = result



#-----------------------------------------------------------------------------
# Results
#-----------------------------------------------------------------------------

'''The 100 most positive signed and most negative signed words'''

runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))

#-----------------------------------------------------------------------------
# Apply Lexicon
#-----------------------------------------------------------------------------

'''Apply the Lexicon to score the transcripts of the video clips.'''

from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words
#Import Data re: transcripts of video snippets

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
hansardVideos = pd.read_csv(gitHub, encoding='utf-8')

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
countedWordsList = []
    

'''A loop for cycling through the list of rows in the hansardVideo
Transcripts.'''
    
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
    '''break the sentence into words'''
    sentence_words = sentence_to_wordlist(sentence)
    '''initialize variables'''
    sentiment = 0 #positivity minus negativity
    sentencePolarity = 0 #absolute values of positivity minus negativity
    wordPolaritySummed = 0 #sum of absolute value of word polarities
    countedWords = 0
    
    '''for every word in the sentence, subtract the sum of its cosine 
    similarity to the negative seed words from the sum of its cosine
    similarity to the positive seed words, and then sum the difference
    across all words in the sentence.'''
    
    for word in sentence_words:

        try:

            word_model = model1[word]

            pos1 = np.dot(word_model, correct) / (np.linalg.norm(word_model) * np.linalg.norm(correct))

            neg1 = np.dot(word_model, wrong) / (np.linalg.norm(word_model) * np.linalg.norm(wrong))


            pos = sum([pos1]) 
            neg = sum([neg1]) 
            posneg = pos - neg
            sentiment += posneg
            wordPolaritySummed += abs(posneg)
            countedWords +=1
            

        except:
            
            #handful of garbage words -- did not meet minimum word threschold
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    
    i+=1


'''output to csv file'''
    
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
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vCorrectWrongOnly.csv", sep=',', encoding='utf-8')


##############################################################################
#-----------------------------------------------------------------------------
# Replicating Sentiment Analysis with Best/Worst
#-----------------------------------------------------------------------------
##############################################################################




#-----------------------------------------------------------------------------
# Seed Words (Adapted from Turney and Littman)
#-----------------------------------------------------------------------------

best = model1['best']

worst = model1['worst']


vocab = list(model1.wv.vocab.keys()) #the full vocabulary of Google News


# an empty list for storing wights and an empty dictionary for linking
# weights and words

runningTally=[]
dictOfWeights = {}

#-----------------------------------------------------------------------------
# Model
#-----------------------------------------------------------------------------

'''for every word in the hansard, calculate its cosine similarity to the 
lists of positive words and negative words, then substract the sum of that
word's cosine simlarity to negative seed words from its cosine similarity to the
postive seed words.''' 

for word in vocab:

    word_model = model1[word]

    pos1 = np.dot(word_model, best) / (np.linalg.norm(word_model) * np.linalg.norm(best))


    neg1 = np.dot(word_model, best) / (np.linalg.norm(word_model) * np.linalg.norm(best))


    pos = sum([pos1])
    neg = sum([neg1])
    posneg = pos-neg
    result = (word, posneg)
    runningTally.append(result)
    dictOfWeights[word] = result



#-----------------------------------------------------------------------------
# Results
#-----------------------------------------------------------------------------

'''The 100 most positive signed and most negative signed words'''

runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))

#-----------------------------------------------------------------------------
# Apply Lexicon
#-----------------------------------------------------------------------------

'''Apply the Lexicon to score the transcripts of the video clips.'''

#remove stopwords.  They are not relevant to sentiment scoring.
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

#Import Data re: transcripts of video snippets

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
hansardVideos = pd.read_csv(gitHub, encoding='utf-8')

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
countedWordsList = []
    

'''A loop for cycling through the list of rows in the hansardVideo
Transcripts.'''
    
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
    '''break the sentence into words'''
    sentence_words = sentence_to_wordlist(sentence)
    '''initialize variables'''
    sentiment = 0 #positivity minus negativity
    sentencePolarity = 0 #absolute values of positivity minus negativity
    wordPolaritySummed = 0 #sum of absolute value of word polarities
    countedWords = 0
    
    '''for every word in the sentence, subtract the sum of its cosine 
    similarity to the negative seed words from the sum of its cosine
    similarity to the positive seed words, and then sum the difference
    across all words in the sentence.'''
    
    for word in sentence_words:

        try:

            word_model = model1[word]

            pos1 = np.dot(word_model, best) / (np.linalg.norm(word_model) * np.linalg.norm(best))

            neg1 = np.dot(word_model, worst) / (np.linalg.norm(word_model) * np.linalg.norm(worst))


            pos = sum([pos1]) 
            neg = sum([neg1]) 
            posneg = pos - neg
            sentiment += posneg
            wordPolaritySummed += abs(posneg)
            countedWords +=1
            

        except:
            
            #handful of garbage words -- did not meet minimum word threschold
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    
    i+=1


'''output to csv file'''
    
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
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vBestWorstOnly.csv", sep=',', encoding='utf-8')


##############################################################################
#-----------------------------------------------------------------------------
# Replicating Sentiment Analysis with Here/There
#-----------------------------------------------------------------------------
##############################################################################




#-----------------------------------------------------------------------------
# Seed Words (Adapted from Turney and Littman)
#-----------------------------------------------------------------------------

here = model1['here']

there = model1['there']


vocab = list(model1.wv.vocab.keys()) #the full vocabulary of Google News


# an empty list for storing wights and an empty dictionary for linking
# weights and words

runningTally=[]
dictOfWeights = {}

#-----------------------------------------------------------------------------
# Model
#-----------------------------------------------------------------------------

'''for every word in the hansard, calculate its cosine similarity to the 
lists of positive words and negative words, then substract the sum of that
word's cosine simlarity to negative seed words from its cosine similarity to the
postive seed words.''' 

for word in vocab:

    word_model = model1[word]

    pos1 = np.dot(word_model, here) / (np.linalg.norm(word_model) * np.linalg.norm(here))


    neg1 = np.dot(word_model, there) / (np.linalg.norm(word_model) * np.linalg.norm(there))


    pos = sum([pos1])
    neg = sum([neg1])
    posneg = pos-neg
    result = (word, posneg)
    runningTally.append(result)
    dictOfWeights[word] = result



#-----------------------------------------------------------------------------
# Results
#-----------------------------------------------------------------------------

'''The 100 most positive signed and most negative signed words'''

runningTally = sorted(runningTally, key=itemgetter(1), reverse=True)
print("Top Positive:", runningTally[:100])
print("Top Negative:", runningTally[len(runningTally)-100:])
print("Total Vocabulary Size:", len(vocab))

#-----------------------------------------------------------------------------
# Apply Lexicon
#-----------------------------------------------------------------------------

'''Apply the Lexicon to score the transcripts of the video clips.'''

#remove stopwords.  They are not relevant to sentiment scoring.
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def sentence_to_wordlist(sentence, remove_stopwords=False):
    sentence_text = re.sub(r'[^\w\s]',' ', sentence)
    words = sentence_text.lower().split()

    for word in words: #Remove Stopwords (Cochrane)
        if word in stopwords:
            words.remove(word)

    return words

#Import Data re: transcripts of video snippets

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
hansardVideos = pd.read_csv(gitHub, encoding='utf-8')

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
countedWordsList = []
    

'''A loop for cycling through the list of rows in the hansardVideo
Transcripts.'''
    
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
    '''break the sentence into words'''
    sentence_words = sentence_to_wordlist(sentence)
    '''initialize variables'''
    sentiment = 0 #positivity minus negativity
    sentencePolarity = 0 #absolute values of positivity minus negativity
    wordPolaritySummed = 0 #sum of absolute value of word polarities
    countedWords = 0
    
    '''for every word in the sentence, subtract the sum of its cosine 
    similarity to the negative seed words from the sum of its cosine
    similarity to the positive seed words, and then sum the difference
    across all words in the sentence.'''
    
    for word in sentence_words:

        try:

            word_model = model1[word]

            pos1 = np.dot(word_model, here) / (np.linalg.norm(word_model) * np.linalg.norm(here))

            neg1 = np.dot(word_model, there) / (np.linalg.norm(word_model) * np.linalg.norm(there))


            pos = sum([pos1]) 
            neg = sum([neg1]) 
            posneg = pos - neg
            sentiment += posneg
            wordPolaritySummed += abs(posneg)
            countedWords +=1
            

        except:
            
            #handful of garbage words -- did not meet minimum word threschold
            print("Warning! Word: ", word, " from speech: ", i, " not in w2v model!")

            continue

    sentimentList.append(sentiment)
    wordPolaritySummedList.append(wordPolaritySummed)   
    sentencePolarityList.append(abs(sentiment))
    countedWordsList.append(countedWords)

    
    i+=1


'''output to csv file'''
    
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
                               'countedWords': countedWordsList})
                               





w2vScores.to_csv("w2vHereThereOnly.csv", sep=',', encoding='utf-8')





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 06:06:37 2019

@author: ludovic rheault with cochrane """

import pandas as pd
import numpy as np
import pickle
import fastText 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re



# Library used to preprocess the texts (already done)
import spacy
nlp = spacy.load('en')

def process(text):
    doc = nlp(text)
    text = ' '.join([w.lemma_ for w in doc if not w.is_punct and not w.is_stop])
    text = text.replace('-PRON-', '') #remocing Spacy lemma convention for pronouns
    return text


#=======================================================#
# Fitting the SVM model
# Imdb dataset
#=======================================================#

# To build tfidf matrix
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)

# Fitting model on the training data
with open('training_imdb.csv') as f:
    training = f.read().splitlines()
training=[(0, t.replace('__label__Negative ','')) if t.startswith('__label__Negative') else (1, t.replace('__label__Positive ','')) for t in training]
y = [l for l,_ in training]
X = [t for _,t in training]
X = vectorizer.fit_transform(X)
kbest = SelectKBest(chi2, k=2000)
X = kbest.fit_transform(X, y)

clf = LinearSVC()
clf.fit(X, y)

# Evaluating the model
with open('testing_imdb.csv') as f:
    testing = f.read().splitlines()
testing=[(0, t.replace('__label__Negative ','')) if t.startswith('__label__Negative') else (1, t.replace('__label__Positive ','')) for t in testing]
y_test = [l for l,_ in testing]
X_test = [t for _,t in testing]
X_test = vectorizer.transform(X_test)
X_test = kbest.transform(X_test)

yhat = clf.predict(X_test)
acc = metrics.accuracy_score(y_test, yhat)
f1 = metrics.f1_score(y_test, yhat)
precision = metrics.precision_score(y_test, yhat)
recall = metrics.recall_score(y_test, yhat)
print(acc)
print(f1)
print(precision)
print(recall)

# Saving model
with open('svm_imdb.pkl', 'wb') as fout:
    pickle.dump((vectorizer, kbest, clf), fout)

#------------------------------------------
# Predicting sentiment of Hansard sentences
#------------------------------------------
    
# Read Data    

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/hansardExtractedVideoTranscripts.csv'
df = pd.read_table(gitHub, sep=',', header=0)


# Applying Processing
preProcessed = []
for item in df['english']:
    preProcessed.append(process(item))

df['preprocessed'] = preProcessed



texts = df.preprocessed.tolist()
texts = vectorizer.transform(texts)
texts = kbest.transform(texts)
df['svm_imdb'] = clf.predict(texts)
df['svm_imdb'] = df.svm_imdb.replace({0:'Negative', 1:'Positive'})

#=======================================================#
# Predictions from fastText model
#=======================================================#

# Loading model
fasttext_model = fastText.load_model('fasttext_imdb.bin') 


# Adding predictions from fastText
texts = df.preprocessed.tolist() #de-vectorizing texts (see above)

fasttext_imdb = []
fasttext_imdbWeights = []

for p in texts:
    prediction = fasttext_model.predict(p)
    weight= prediction[1]
    verdict=str(prediction[0])   
    if '__label__Negative' in verdict:
        verdict = 'Negative'
        weight = weight*-1
    elif 'Positive' in verdict:
        verdict = 'Positive'
    else:
        print("Missing Estimate!!: ", p)
    fasttext_imdb.append(verdict)
    weight = str(weight)
    weight = weight.replace("[","")
    weight = weight.replace("]","")
    fasttext_imdbWeights.append(weight)
    

df['fasttext_imbd'] = list(item for item in fasttext_imdb)
df['fasttext_imbdWeight'] = list(item for item in fasttext_imdbWeights)
  
# Saving Hansard file with predictions
df.to_csv('hansardExtractedVideoTranscripts_SVMFastText.csv', index=False, sep=',')


# Evaluating fastText model accuracy

with open('testing_imdb.csv') as f:
    IMDBclassified = f.read().splitlines() #read classified imdb reviews
    

IMDBunclassified = []
IMDBclassifiedScores = [] #list holders


for n, i in enumerate(IMDBclassified): #remove classification labels form imdb 
    if i.startswith("__label__Negative "):
        #remove known classification for unclassified
        IMDBunclassified.append(IMDBclassified[n].replace('__label__Negative ', ''))
        IMDBclassifiedScores.append(0)
    elif i.startswith("__label__Positive "):
        IMDBunclassified.append(IMDBclassified[n].replace('__label__Positive ', ''))
        IMDBclassifiedScores.append(1)
    else:
        print("Flag! Line: ", n, " with text ", i, " Unclassified in IMDB Corpus")


IMDBFastTextScore = []
for review in IMDBunclassified:
    check = list(fasttext_model.predict(review)[0])   
    if check[0] == '__label__Positive':
        IMDBFastTextScore.append(1)
    elif check[0] == '__label__Negative':
        IMDBFastTextScore.append(0)
    else:
        print("Warning! No FastText Generated for: ", review)
    

acc = metrics.accuracy_score(IMDBclassifiedScores, IMDBFastTextScore)
f1 = metrics.f1_score(IMDBclassifiedScores, IMDBFastTextScore)
precision = metrics.precision_score(IMDBclassifiedScores, IMDBFastTextScore)
recall = metrics.recall_score(IMDBclassifiedScores, IMDBFastTextScore)

print("Fast Text IMDB Accuracy")
print(acc)
print(f1)
print(precision)
print(recall)

#=======================================================#
# Fitting the SVM model
# Stanford dataset
#=======================================================#

# To build tfidf matrix
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)

# Fitting model on the training data
with open('training_stanford.csv') as f:
    training = f.read().splitlines()
training=[(0, t.replace('__label__Negative ','')) if t.startswith('__label__Negative') else (1, t.replace('__label__Positive ','')) for t in training]
y = [l for l,_ in training]
X = [t for _,t in training]
X = vectorizer.fit_transform(X)
kbest = SelectKBest(chi2, k=2000)
X = kbest.fit_transform(X, y)

clf = LinearSVC(C=100)
clf.fit(X, y)

# Evaluating the model
with open('testing_stanford.csv') as f:
    testing = f.read().splitlines()
testing=[(0, t.replace('__label__Negative ','')) if t.startswith('__label__Negative') else (1, t.replace('__label__Positive ','')) for t in testing]
y_test = [l for l,_ in testing]
X_test = [t for _,t in testing]
X_test = vectorizer.transform(X_test)
X_test = kbest.transform(X_test)

yhat = clf.predict(X_test)
acc = metrics.accuracy_score(y_test, yhat)
f1 = metrics.f1_score(y_test, yhat)
precision = metrics.precision_score(y_test, yhat)
recall = metrics.recall_score(y_test, yhat)
print("IMDB Estimates Model Accuracy")
print(acc)
print(f1)
print(precision)
print(recall)

# Saving model
with open('svm_stanford.pkl', 'wb') as fout:
    pickle.dump((vectorizer, kbest, clf), fout)

# Predicting sentiment of Hansard sentences
texts = df.preprocessed.tolist()
texts = vectorizer.transform(texts)
texts = kbest.transform(texts)
df['svm_stanford'] = clf.predict(texts)
df['svm_stanford'] = df.svm_imdb.replace({0:'Negative', 1:'Positive'})

#=======================================================#
# Predictions from fastText model
#=======================================================#

# Loading model
fasttext_model = fastText.load_model('fasttext_stanford.bin') #Cochrane edited

# Adding predictions from fastText
texts = df.preprocessed.tolist() #de-vectorizing texts (see above)

fasttext_stanford = []
fasttext_stanfordWeights = []
for p in texts:
    prediction = fasttext_model.predict(p)
    weight = prediction[1]
    verdict=str(prediction[0]) 
    if '__label__Negative' in verdict:
        verdict = 'Negative' 
        weight = weight*-1
    elif '__label__Positive' in verdict:
        verdict = 'Positive'
    else:
        print('Missing Estimate!!: ', p)
    weight = str(weight)
    weight = weight.replace("[","")
    weight = weight.replace("]","")
    fasttext_stanford.append(verdict)
    fasttext_stanfordWeights.append(weight)
    

df['fasttext_stanford'] = list(item for item in fasttext_stanford)
df['fasttext_stanfordWeights'] = list(item for item in fasttext_stanfordWeights)
  


# Evaluating fastText model accuracy

with open('testing_stanford.csv') as f:
    StanfordClassified = f.read().splitlines() #read classified Stanford reviews
    

StanfordUnclassified = []
StanfordClassifiedScores = [] 
newStanfordClassified = [] # will exclude handful of unclassified tweets in Stanford corpus

for n, i in enumerate(StanfordClassified): #remove classification labels form imdb 
    if i.startswith("__label__Negative "):
        #remove known classification from unclassified
        StanfordUnclassified.append(StanfordClassified[n].replace('__label__Negative ', ''))
        StanfordClassifiedScores.append(0)
        newStanfordClassified.append(StanfordClassified[n])
    elif i.startswith("__label__Positive "):
        StanfordUnclassified.append(StanfordClassified[n].replace('__label__Positive ', ''))
        StanfordClassifiedScores.append(1)
        newStanfordClassified.append(StanfordClassified[n])
    else:
        print("Flag! Line: ", n, " with text ", i, " Unclassified in Stanford Corpus. Dropping")


StanfordFastTextScore = []
for review in StanfordUnclassified:
    check = list(fasttext_model.predict(review)[0])   
    if check[0] == '__label__Positive':
        StanfordFastTextScore.append(1)
    elif check[0] == '__label__Negative':
        StanfordFastTextScore.append(0)
    else:
        print("Warning! No FastText Generated for: ", review)
    

acc = metrics.accuracy_score(StanfordClassifiedScores, StanfordFastTextScore)
f1 = metrics.f1_score(StanfordClassifiedScores, StanfordFastTextScore)
precision = metrics.precision_score(StanfordClassifiedScores, StanfordFastTextScore)
recall = metrics.recall_score(StanfordClassifiedScores, StanfordFastTextScore)
print("Stanford Estimates Model Accuracy")
print(acc)
print(f1)
print(precision)
print(recall)



#######################################################
#Apply Vader and LIWC Dictionaries
#######################################################


#The popular VADER library for Python, which performs valence shifting for negation words.
# More adapted to social media.
vader = SentimentIntensityAnalyzer()

# Negation words that could be used to account for valence shifting.
negation = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
     "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
     "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
     "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
     "neednt", "needn't", "never", "none", "nope", "nor", "not", "no", "nothing", "nowhere",
     "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
     "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
     "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]

# To compute scores from dictionaries with wild card symbols for inflexions. 
def sentiment_scores(text, lexicon):
    text = text.lower()
    count = 0
    for word in lexicon:
        if word.endswith('*'):
            count += len([t for t in text if t.startswith(word[:-1])])
        else:
            count += text.count(word) 
    score = (count)/len(text)
    return score

# Rescaling variable.
def rescale(x, newmin, newmax, oldmin=None, oldmax=None):
    if not oldmin:
        oldmin = min(x)
    if not oldmax:
        oldmax = max(x)
    return (((x - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin


# The LIWC positive and negative emotion dictionaries.
# Note: these are a part of proprietary software that we don't have permission
# to share. To reproduce our analysis here, visit http://liwc.wpengine.com/
with open('liwc2015_positive.txt') as f:
    liwc_pos = f.read().splitlines()
with open('liwc2015_negative.txt') as f:
    liwc_neg = f.read().splitlines()

# Adding a LIWC sentiment score, and the VADER compound score.
df['liwc'] = df.preprocessed.apply(lambda x: sentiment_scores(x, liwc_pos) - sentiment_scores(x, liwc_neg))
df['vader'] = df.preprocessed.apply(lambda x: vader.polarity_scores(x.lower())['compound'])

# SVM model fitted with Platt probabilities on the IMDb dataset.
with open('svm_imdb_probs.pkl', 'rb') as f:
    vectorizer, kbest, svm = pickle.load(f)

# Predicting Platt probabilities on Hansard texts.
texts = df.preprocessed.tolist()
texts = vectorizer.transform(texts)
texts = kbest.transform(texts)
df['svm_imdb_probability'] = svm.predict_proba(texts)[:,1]

# Rescaling lexicons between 0 and 10.
df['liwc'] = rescale(df.liwc, 0, 10)
# Vader was already rescaled between -1 and 1.
df['vader'] = rescale(df.vader, newmin=0, newmax=10, oldmin=-1, oldmax=1)


# Saving Hansard file with predictions

#removing '-' in preprocessed, which excel reads as minus when first character


df.to_csv('hansardExtractedVideoTranscripts_SVMFastTextVader.csv', index=False, sep=',')

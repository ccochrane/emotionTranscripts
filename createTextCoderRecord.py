# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:52:38 2018

@author: chriscochrane

A script for creating a record of the video coding from the structured
Qualrics Output
"""
# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np


# -----------------------------------------------------------------------------
# Import Structured Qualtrics Data from Github
# -----------------------------------------------------------------------------

#gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/qualtricsStructured.csv'

sf_coding1 = 'sf_coding1.csv'
sf_coding2 = 'sf_coding2.csv'
cm_coding1 = 'cm_coding1.csv'
cm_coding2 = 'cm_coding2.csv'
jv_coding1 = 'jv_coding1.csv'
jv_coding2 = 'jv_coding2.csv'

sf_coding1 = pd.read_csv(sf_coding1)
sf_coding2 = pd.read_csv(sf_coding2)
cm_coding1 = pd.read_csv(cm_coding1)
cm_coding2 = pd.read_csv(cm_coding2)
jv_coding1 = pd.read_csv(jv_coding1)
jv_coding2 = pd.read_csv(jv_coding2)


## -----------------------------------------------------------------------------
## Creating Functions
## -----------------------------------------------------------------------------


def extractTextRecord(t1_1, t1_2, t2_1, t2_2, t3_1, t3_2):
    '''text coding records randomly shuffled.  Re-arranging on label to
    standardize order.'''
    t1_1 = t1_1.sort_values(['Label'])
    t1_2 = t1_2.sort_values(['Label'])
    t2_1 = t2_1.sort_values(['Label'])
    t2_2 = t2_2.sort_values(['Label'])
    t3_1 = t3_1.sort_values(['Label'])
    t3_2 = t3_2.sort_values(['Label'])
    
#    '''converting label to index'''
#    
    t1_1 = t1_1.set_index('Label')
    t1_2 = t1_2.set_index('Label')
    t2_1 = t2_1.set_index('Label')
    t2_2 = t2_2.set_index('Label')
    t3_1 = t3_1.set_index('Label')
    t3_2 = t3_2.set_index('Label')
    
    t1Act1List = []
    t1Act2List = []
    t1ActAvgList = []
    t2Act1List = []
    t2Act2List = []
    t2ActAvgList = []
    t3Act1List = []
    t3Act2List = []
    t3ActAvgList = []
    t1Sent1List = []
    t1Sent2List = []
    t1SentAvgList = []
    t2Sent1List = []
    t2Sent2List = []
    t2SentAvgList = []
    t3Sent1List = []
    t3Sent2List = []
    t3SentAvgList = []
    videoList =[]
    
    
    
    for row in t1_1.index:
        t1Act1 = t1_1.loc[row,'Activation']
        t1Act2 = t1_2.loc[row,'Activation']
        t1ActAvg = (t1Act1+t1Act2)/2
        t2Act1 = t2_1.loc[row,'Activation']
        t2Act2 = t2_2.loc[row,'Activation']
        t2ActAvg = (t2Act1+t2Act2)/2
        t3Act1 = t3_1.loc[row,'Activation']
        t3Act2 = t3_2.loc[row,'Activation']
        t3ActAvg = (t3Act1+t3Act2)/2
        t1Sent1 = t1_1.loc[row,'Sentiment']
        t1Sent2 = t1_2.loc[row,'Sentiment']
        t1SentAvg = (t1Sent1+t1Sent2)/2
        t2Sent1 = t2_1.loc[row,'Sentiment']
        t2Sent2 = t2_2.loc[row,'Sentiment']
        t2SentAvg = (t2Sent1+t2Sent2)/2
        t3Sent1 = t3_1.loc[row,'Sentiment']
        t3Sent2 = t3_2.loc[row,'Sentiment']
        t3SentAvg = (t3Sent1+t3Sent2)/2
        
        
        t1Act1List.append(t1Act1)
        t1Act2List.append(t1Act2)
        t1ActAvgList.append(t1ActAvg)
        t2Act1List.append(t2Act1)
        t2Act2List.append(t2Act2)
        t2ActAvgList.append(t2ActAvg)
        t3Act1List.append(t3Act1)
        t3Act2List.append(t3Act2)
        t3ActAvgList.append(t3ActAvg)
        t1Sent1List.append(t1Sent1)
        t1Sent2List.append(t1Sent2)
        t1SentAvgList.append(t1SentAvg)
        t2Sent1List.append(t2Sent1)
        t2Sent2List.append(t2Sent2)
        t2SentAvgList.append(t2SentAvg)
        t3Sent1List.append(t3Sent1)
        t3Sent2List.append(t3Sent2)
        t3SentAvgList.append(t3SentAvg)
        
        videoList.append(t1_2.loc[row, 'Video'])
        
    textAverages = pd.DataFrame({'t1SentAvg': t1SentAvgList,
                              't2SentAvg': t2SentAvgList,
                              't3SentAvg': t3SentAvgList,                                 
                              't1ActAvg': t1ActAvgList,
                              't2ActAvg': t2ActAvgList,
                              't3ActAvg': t3ActAvgList,
                              't1Sent1': t1Sent1List,
                              't1Sent2': t1Sent2List,
                              't2Sent1': t2Sent1List,
                              't2Sent2': t2Sent2List,
                              't3Sent1': t3Sent1List,
                              't3Sent2': t3Sent2List,
                              't1Act1': t1Act1List,
                              't1Act2': t1Act2List,
                              't2Act1': t2Act1List,
                              't2Act2': t2Act2List,
                              't3Act1': t3Act1List,
                              't3Act2': t3Act2List,
                              'Video': videoList
                              })
    
    textAverages.set_index('Video', inplace=True)
    
    
    return(textAverages)
    
  
## -----------------------------------------------------------------------------
## Apply Functions
## -----------------------------------------------------------------------------

textRecord = extractTextRecord(sf_coding1, sf_coding2,
                  cm_coding1, cm_coding2,
                  jv_coding1, jv_coding2)
    
## -----------------------------------------------------------------------------
## Output Data
## -----------------------------------------------------------------------------

textRecord.to_csv('textCoderAverages.csv', encoding='utf-8')


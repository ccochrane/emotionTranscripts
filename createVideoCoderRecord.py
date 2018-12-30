#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 09:32:45 2018

@author: chriscochrane
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 13:57:55 2018

@author: chriscochrane
"""

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:26:50 2018

@author: chriscochrane
"""

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

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/qualtricsStructured.csv'

qualtricsStructured = pd.read_csv(gitHub)

# -----------------------------------------------------------------------------
# Creating Functions
# -----------------------------------------------------------------------------

'''Function for selecting first two codes per coder,
to align with text coders, where each video was coded
only twice.'''


def chooseFirstTwo(coderData):
    '''Counting the video order to get the first two'''
    coderData['Sequence'] = coderData.groupby([coderData['Coder'], coderData['Video']]).cumcount()
    '''selecting the first two'''
    firstTwo = coderData.loc[coderData['Sequence'] <= 1]

    return (firstTwo)


'''Function for selecting average scores for videos'''


def findVideoAverages(firstTwo):
    '''Replicating the DataFrame explicity for the purpose of duplicating
    the Sentiment and Activation Columns without triggering a `set on slice'
    warning'''
    firstTwo = pd.DataFrame({'Sentiment': firstTwo['Sentiment'],
                             'Sentiment1': firstTwo['Sentiment'],
                             'Activation': firstTwo['Activation'],
                             'Activation1': firstTwo['Activation'],
                             'Sequence': firstTwo['Sequence'],
                             'Coder': firstTwo['Coder'],
                             'Video': firstTwo['Video']
                             })
    
    '''A new dataframe of aggregates structured by coder and video.  Takes
    the mean of sentiment and activation for each video and coder, the first 
    activation and sentiment score each coder assigned to each video, and the
    max Sequence, which tells whether a coder coded that video more than once.
    '''
    videoAverages = firstTwo.groupby(['Coder', 'Video'], as_index=False).agg({
        'Sentiment': 'mean',
        'Sentiment1': 'first',
        'Activation1': 'first',
        'Activation': 'mean',
        'Sequence': 'max'
    })

    '''dictionaries with empty entries for each video'''
    PORBSentAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    JSSentAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    MSSentAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    PORBSent1 = dict((el, np.NaN) for el in videoAverages["Video"])
    JSSent1 = dict((el, np.NaN) for el in videoAverages["Video"])
    MSSent1 = dict((el, np.NaN) for el in videoAverages["Video"])
    PORBSent2 = dict((el, np.NaN) for el in videoAverages["Video"])
    JSSent2 = dict((el, np.NaN) for el in videoAverages["Video"])
    MSSent2 = dict((el, np.NaN) for el in videoAverages["Video"])
    PORBActAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    JSActAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    MSActAvg = dict((el, np.NaN) for el in videoAverages["Video"])
    PORBAct1 = dict((el, np.NaN) for el in videoAverages["Video"])
    JSAct1 = dict((el, np.NaN) for el in videoAverages["Video"])
    MSAct1 = dict((el, np.NaN) for el in videoAverages["Video"])
    PORBAct2 = dict((el, np.NaN) for el in videoAverages["Video"])
    JSAct2 = dict((el, np.NaN) for el in videoAverages["Video"])
    MSAct2 = dict((el, np.NaN) for el in videoAverages["Video"])

    '''loop for populating dictionaries.  Re-creates a second video score,
    if a video is coded more than once, from the average score (calculated 
    above) and the first video score.'''
    for item in videoAverages.index:
        video = videoAverages.loc[item,'Video']
        sentiment = videoAverages.loc[item,'Sentiment']
        activation = videoAverages.loc[item,'Activation']
        if videoAverages.loc[item,'Sequence'] == 0:
            sentiment1 = videoAverages.loc[item,'Sentiment1']
            activation1 = videoAverages.loc[item,'Activation1']
            sentiment2 = np.NaN
            activation2 = np.NaN
        else:
            sentiment1 = videoAverages.loc[item, 'Sentiment1']
            activation1 = videoAverages.loc[item, 'Activation1']
            sentiment2 = 2*sentiment-sentiment1
            activation2 = 2*activation-activation1


        if videoAverages.loc[item,'Coder'] == "P-O R. B.":
            PORBSentAvg[video] = sentiment
            PORBActAvg[video] = activation
            PORBSent1[video] = sentiment1
            PORBSent2[video] = sentiment2
            PORBAct1[video] = activation1
            PORBAct2[video] = activation2

        elif videoAverages.loc[item,'Coder'] == "JS":
            JSSentAvg[video] = sentiment
            JSActAvg[video] = activation
            JSSent1[video] = sentiment1
            JSSent2[video] = sentiment2
            JSAct1[video] = activation1
            JSAct2[video] = activation2

        elif videoAverages.loc[item,'Coder'] == "MS":
            MSSentAvg[video] = sentiment
            MSActAvg[video] = activation
            MSSent1[video] = sentiment1
            MSSent2[video] = sentiment2
            MSAct1[video] = activation1
            MSAct2[video] = activation2


    videoAverages = pd.DataFrame({'v1SentAvg': pd.Series(PORBSentAvg),
                                  'v3SentAvg': pd.Series(JSSentAvg),
                                  'v2SentAvg': pd.Series(MSSentAvg),
                                  'v1ActAvg': pd.Series(PORBActAvg),
                                  'v3ActAvg': pd.Series(JSActAvg),
                                  'v2ActAvg': pd.Series(MSActAvg),
                                  'v1Sent1': pd.Series(PORBSent1),
                                  'v1Sent2': pd.Series(PORBSent2),
                                  'v3Sent1': pd.Series(JSSent1),
                                  'v3Sent2': pd.Series(JSSent2),
                                  'v2Sent1': pd.Series(MSSent1),
                                  'v2Sent2': pd.Series(MSSent2),
                                  'v1Act1': pd.Series(PORBAct1),
                                  'v1Act2': pd.Series(PORBAct2),
                                  'v3Act1': pd.Series(JSAct1),
                                  'v3Act2': pd.Series(JSAct2),
                                  'v2Act1': pd.Series(MSAct1),
                                  'v2Act2': pd.Series(MSAct2),
                                  })
  
    return videoAverages


# -----------------------------------------------------------------------------
# Apply Functions
# -----------------------------------------------------------------------------

videoCoderFirstTwo = chooseFirstTwo(qualtricsStructured)
videoCoderAverages = findVideoAverages(videoCoderFirstTwo)

# -----------------------------------------------------------------------------
# Output Data
# -----------------------------------------------------------------------------


videoCoderAverages.to_csv('videoCoderAverages.csv', encoding='utf-8')



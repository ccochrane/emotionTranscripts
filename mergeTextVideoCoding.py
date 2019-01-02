#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 06:49:07 2019

@author: chriscochrane
"""

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

import pandas as pd



# -----------------------------------------------------------------------------
# Import Data
# -----------------------------------------------------------------------------

gitHubText = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/textCoderAverages.csv'
gitHubVideo = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/videoCoderAverages.csv'


textCoderAverages = pd.read_csv(gitHubText)
videoCoderAverages = pd.read_csv(gitHubVideo)

# -----------------------------------------------------------------------------
# Define Function for Merging
# -----------------------------------------------------------------------------

fullCodingData = textCoderAverages.merge(videoCoderAverages, how='outer'
                       ,on='Video')

fullCodingData.to_csv('fullCodingData.csv', encoding='utf-8')
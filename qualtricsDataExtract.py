#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:26:50 2018

@author: chriscochrane
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:52:38 2018

@author: chriscochrane

A script for extracting meaningful information from the dog's breakfast
that Qualtrics outputs.  
"""
#-----------------------------------------------------------------------------
# Initialization
#-----------------------------------------------------------------------------

import pandas as pd

#-----------------------------------------------------------------------------
# Import Raw Qualtrics Data from Github
#-----------------------------------------------------------------------------

gitHub = 'https://raw.githubusercontent.com/ccochrane/emotionParliament/master/emotionInHansard_December%2B20%252C%2B2018_14.52.csv'
qualtricsRaw = pd.read_csv(gitHub)

#-----------------------------------------------------------------------------
# Create a Parsing Function
#-----------------------------------------------------------------------------

'''Function for identifying variables in the string of Qualtrics output'''
def findStringParts(string, symbol, n):
    string = str(string)
    parts = string.split(symbol, n+1)
    if len(parts)<=n+1:
        return parts
    return parts

#-----------------------------------------------------------------------------
# Create Empty Lists to Store Data
#-----------------------------------------------------------------------------

'''Empty Lists'''
videoList = []
coderList = []
sentimentList = []
activationList = []
angerList = []
disgustList = []
fearList = []
happinessList = []
sadnessList = []
surpriseList = []

#-----------------------------------------------------------------------------
# Extract Data Row-by-Row
#-----------------------------------------------------------------------------


for i in range(4,len(qualtricsRaw)):
    if qualtricsRaw['distributionChannel'][i] != "preview": #drop previews
        coder = qualtricsRaw['QID78_TEXT'][i]
        if coder == "js":
            coder = "JS"
        #-----------------
        # Bloc A
        #-----------------
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_9z3f3SVI5D1eOk5_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocA_DO = findStringParts(qualtricsRaw['BL_9z3f3SVI5D1eOk5_DO'][i], '|', numBars) 
        blocA_title_vid1 = blocA_DO[0] # The first video title
        blocA_title_vid2 = blocA_DO[1] # The second video title
        '''arousal code for first video'''
        blocA_act_vid1 = qualtricsRaw['QID23_1'][i] 
        '''arousal code for second video'''
        blocA_act_vid2 = qualtricsRaw['QID23_2'][i] 
        '''sentiment code for first video'''
        blocA_sent_vid1 = qualtricsRaw['QID26_1'][i] 
        '''sentiment code for second video'''
        blocA_sent_vid2 = qualtricsRaw['QID26_2'][i] 
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID54#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID54#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID54#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID54#1_4'][i],',',2)
        sadness = findStringParts(qualtricsRaw['QID54#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID54#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocA_anger_vid1 = 1
            if len(anger)== 2:
                blocA_anger_vid2 = 1
            else:
                blocA_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocA_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocA_anger_vid2 = 1
            else:
                blocA_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocA_disgust_vid1 = 1
            if len(disgust) == 2:
                blocA_disgust_vid2 = 1
            else:
                blocA_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocA_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocA_disgust_vid2 = 1
            else:
                blocA_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocA_fear_vid1 = 1
            if len(fear) == 2:
                blocA_fear_vid2 = 1
            else:
                blocA_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocA_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocA_fear_vid2 = 1
            else:
                blocA_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocA_happiness_vid1 = 1
            if len(happiness) == 2:
                blocA_happiness_vid2 = 1
            else:
                blocA_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocA_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocA_happiness_vid2 = 1
            else:
                blocA_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocA_sadness_vid1 = 1
            if len(sadness) == 2:
                blocA_sadness_vid2 = 1
            else:
                blocA_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocA_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocA_sadness_vid2 = 1
            else:
                blocA_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocA_surprise_vid1 = 1
            if len(surprise) == 2:
                blocA_surprise_vid2 = 1
            else:
                blocA_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocA_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocA_surprise_vid2 = 1
            else:
                blocA_surprise_vid2 = 0
        
        '''Add Bloc A data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocA_title_vid1)
        sentimentList.append(blocA_sent_vid1)
        activationList.append(blocA_act_vid1)
        angerList.append(blocA_anger_vid1)
        disgustList.append(blocA_disgust_vid1)
        fearList.append(blocA_fear_vid1)
        happinessList.append(blocA_happiness_vid1)
        sadnessList.append(blocA_sadness_vid1)
        surpriseList.append(blocA_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocA_title_vid2)
        sentimentList.append(blocA_sent_vid2)
        activationList.append(blocA_act_vid2)
        angerList.append(blocA_anger_vid2)
        disgustList.append(blocA_disgust_vid2)
        fearList.append(blocA_fear_vid2)
        happinessList.append(blocA_happiness_vid2)
        sadnessList.append(blocA_sadness_vid2)
        surpriseList.append(blocA_surprise_vid2)

        #-----------------
        # Bloc B
        #-----------------
        
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_6Rb4ytpLTIRc2ot_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocB_DO = findStringParts(qualtricsRaw['BL_6Rb4ytpLTIRc2ot_DO'][i], '|', numBars) 
        blocB_title_vid1 = blocB_DO[0] # The first video title
        blocB_title_vid2 = blocB_DO[1] # The second video title
        # *** FIXED! Sentiment and Activation Labels Reversed in Qualtrics ***
        '''arousal code for first video'''
        blocB_act_vid1 = qualtricsRaw['QID3450_1'][i] 
        '''arousal code for second video'''
        blocB_act_vid2 = qualtricsRaw['QID3450_2'][i] 
        '''sentiment code for first video'''
        blocB_sent_vid1 = qualtricsRaw['QID3451_1'][i]
        '''sentiment code for second video'''
        blocB_sent_vid2 = qualtricsRaw['QID3451_2'][i] 
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID3452#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID3452#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID3452#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID3452#1_4'][i],',',2)
        sadness = findStringParts(qualtricsRaw['QID3452#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID3452#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocB_anger_vid1 = 1
            if len(anger)== 2:
                blocB_anger_vid2 = 1
            else:
                blocB_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocB_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocB_anger_vid2 = 1
            else:
                blocB_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocB_disgust_vid1 = 1
            if len(disgust) == 2:
                blocB_disgust_vid2 = 1
            else:
                blocB_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocB_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocB_disgust_vid2 = 1
            else:
                blocB_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocB_fear_vid1 = 1
            if len(fear) == 2:
                blocB_fear_vid2 = 1
            else:
                blocB_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocB_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocB_fear_vid2 = 1
            else:
                blocB_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocB_happiness_vid1 = 1
            if len(happiness) == 2:
                blocB_happiness_vid2 = 1
            else:
                blocB_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocB_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocB_happiness_vid2 = 1
            else:
                blocB_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocB_sadness_vid1 = 1
            if len(sadness) == 2:
                blocB_sadness_vid2 = 1
            else:
                blocB_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocB_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocB_sadness_vid2 = 1
            else:
                blocB_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocB_surprise_vid1 = 1
            if len(surprise) == 2:
                blocB_surprise_vid2 = 1
            else:
                blocB_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocB_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocB_surprise_vid2 = 1
            else:
                blocB_surprise_vid2 = 0
        
        '''Add Bloc B data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocB_title_vid1)
        sentimentList.append(blocB_sent_vid1)
        activationList.append(blocB_act_vid1)
        angerList.append(blocB_anger_vid1)
        disgustList.append(blocB_disgust_vid1)
        fearList.append(blocB_fear_vid1)
        happinessList.append(blocB_happiness_vid1)
        sadnessList.append(blocB_sadness_vid1)
        surpriseList.append(blocB_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocB_title_vid2)
        sentimentList.append(blocB_sent_vid2)
        activationList.append(blocB_act_vid2)
        angerList.append(blocB_anger_vid2)
        disgustList.append(blocB_disgust_vid2)
        fearList.append(blocB_fear_vid2)
        happinessList.append(blocB_happiness_vid2)
        sadnessList.append(blocB_sadness_vid2)
        surpriseList.append(blocB_surprise_vid2)     

        #-----------------
        # Bloc C
        #-----------------
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_9YmtLZfF0ecSpuJ_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocC_DO = findStringParts(qualtricsRaw['BL_9YmtLZfF0ecSpuJ_DO'][i], '|', numBars) 
        blocC_title_vid1 = blocC_DO[0] # The first video title
        blocC_title_vid2 = blocC_DO[1] # The second video title
        '''arousal code for first video'''
        blocC_act_vid1 = qualtricsRaw['QID1055_1'][i]  
        '''arousal code for second video'''
        blocC_act_vid2 = qualtricsRaw['QID1055_2'][i]
        '''sentiment code for first video'''
        blocC_sent_vid1 = qualtricsRaw['QID1056_1'][i]
        '''sentiment code for second video'''
        blocC_sent_vid2 = qualtricsRaw['QID1056_2'][i]
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID1057#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID1057#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID1057#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID1057#1_4'][i],',',2)
        sadness = findStringParts(qualtricsRaw['QID1057#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID1057#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocC_anger_vid1 = 1
            if len(anger)== 2:
                blocC_anger_vid2 = 1
            else:
                blocC_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocC_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocC_anger_vid2 = 1
            else:
                blocC_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocC_disgust_vid1 = 1
            if len(disgust) == 2:
                blocC_disgust_vid2 = 1
            else:
                blocC_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocC_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocC_disgust_vid2 = 1
            else:
                blocC_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocC_fear_vid1 = 1
            if len(fear) == 2:
                blocC_fear_vid2 = 1
            else:
                blocC_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocC_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocC_fear_vid2 = 1
            else:
                blocC_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocC_happiness_vid1 = 1
            if len(happiness) == 2:
                blocC_happiness_vid2 = 1
            else:
                blocC_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocC_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocC_happiness_vid2 = 1
            else:
                blocC_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocC_sadness_vid1 = 1
            if len(sadness) == 2:
                blocC_sadness_vid2 = 1
            else:
                blocC_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocC_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocC_sadness_vid2 = 1
            else:
                blocC_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocC_surprise_vid1 = 1
            if len(surprise) == 2:
                blocC_surprise_vid2 = 1
            else:
                blocC_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocC_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocC_surprise_vid2 = 1
            else:
                blocC_surprise_vid2 = 0
        
        '''Add Bloc C data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocC_title_vid1)
        sentimentList.append(blocC_sent_vid1)
        activationList.append(blocC_act_vid1)
        angerList.append(blocC_anger_vid1)
        disgustList.append(blocC_disgust_vid1)
        fearList.append(blocC_fear_vid1)
        happinessList.append(blocC_happiness_vid1)
        sadnessList.append(blocC_sadness_vid1)
        surpriseList.append(blocC_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocC_title_vid2)
        sentimentList.append(blocC_sent_vid2)
        activationList.append(blocC_act_vid2)
        angerList.append(blocC_anger_vid2)
        disgustList.append(blocC_disgust_vid2)
        fearList.append(blocC_fear_vid2)
        happinessList.append(blocC_happiness_vid2)
        sadnessList.append(blocC_sadness_vid2)
        surpriseList.append(blocC_surprise_vid2)


        #-----------------
        # BlocD
        #-----------------
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_6rskZu2BNcPiZfL_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocD_DO = findStringParts(qualtricsRaw['BL_6rskZu2BNcPiZfL_DO'][i], '|', numBars) 
        blocD_title_vid1 = blocD_DO[0] # The first video title
        blocD_title_vid2 = blocD_DO[1] # The second video title
        # *** FIXED! Sentiment and Activation Labels Reversed in Qualtrics ***
        '''arousal code for first video'''
        blocD_act_vid1 = qualtricsRaw['QID3454_1'][i] #FIXED!
        '''arousal code for second video'''
        blocD_act_vid2 = qualtricsRaw['QID3454_2'][i] #FIXED!
        '''sentiment code for first video'''
        blocD_sent_vid1 = qualtricsRaw['QID3455_1'][i] #FIXED!
        '''sentiment code for second video'''
        blocD_sent_vid2 = qualtricsRaw['QID3455_2'][i] #FIXED!
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID3456#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID3456#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID3456#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID3456#1_4'][i], ',',2)
        sadness = findStringParts(qualtricsRaw['QID3456#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID3456#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocD_anger_vid1 = 1
            if len(anger)== 2:
                blocD_anger_vid2 = 1
            else:
                blocD_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocD_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocD_anger_vid2 = 1
            else:
                blocD_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocD_disgust_vid1 = 1
            if len(disgust) == 2:
                blocD_disgust_vid2 = 1
            else:
                blocD_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocD_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocD_disgust_vid2 = 1
            else:
                blocD_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocD_fear_vid1 = 1
            if len(fear) == 2:
                blocD_fear_vid2 = 1
            else:
                blocD_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocD_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocD_fear_vid2 = 1
            else:
                blocD_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocD_happiness_vid1 = 1
            if len(happiness) == 2:
                blocD_happiness_vid2 = 1
            else:
                blocD_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocD_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocD_happiness_vid2 = 1
            else:
                blocD_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocD_sadness_vid1 = 1
            if len(sadness) == 2:
                blocD_sadness_vid2 = 1
            else:
                blocD_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocD_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocD_sadness_vid2 = 1
            else:
                blocD_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocD_surprise_vid1 = 1
            if len(surprise) == 2:
                blocD_surprise_vid2 = 1
            else:
                blocD_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocD_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocD_surprise_vid2 = 1
            else:
                blocD_surprise_vid2 = 0
        
        '''Add Bloc D data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocD_title_vid1)
        sentimentList.append(blocD_sent_vid1)
        activationList.append(blocD_act_vid1)
        angerList.append(blocD_anger_vid1)
        disgustList.append(blocD_disgust_vid1)
        fearList.append(blocD_fear_vid1)
        happinessList.append(blocD_happiness_vid1)
        sadnessList.append(blocD_sadness_vid1)
        surpriseList.append(blocD_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocD_title_vid2)
        sentimentList.append(blocD_sent_vid2)
        activationList.append(blocD_act_vid2)
        angerList.append(blocD_anger_vid2)
        disgustList.append(blocD_disgust_vid2)
        fearList.append(blocD_fear_vid2)
        happinessList.append(blocD_happiness_vid2)
        sadnessList.append(blocD_sadness_vid2)
        surpriseList.append(blocD_surprise_vid2)

        #-----------------
        # BlocE
        #-----------------
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_3aS8nqvLjwudQl7_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocE_DO = findStringParts(qualtricsRaw['BL_3aS8nqvLjwudQl7_DO'][i], '|', numBars) 
        blocE_title_vid1 = blocE_DO[0] # The first video title
        blocE_title_vid2 = blocE_DO[1] # The second video title
        '''arousal code for first video'''
        blocE_act_vid1 = qualtricsRaw['QID1060_1'][i] 
        '''arousal code for second video'''
        blocE_act_vid2 = qualtricsRaw['QID1060_2'][i] 
        '''sentiment code for first video'''
        blocE_sent_vid1 = qualtricsRaw['QID1061_1'][i] 
        '''sentiment code for second video'''
        blocE_sent_vid2 = qualtricsRaw['QID1061_2'][i] 
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID1062#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID1062#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID1062#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID1062#1_4'][i], ',',2)
        sadness = findStringParts(qualtricsRaw['QID1062#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID1062#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocE_anger_vid1 = 1
            if len(anger)== 2:
                blocE_anger_vid2 = 1
            else:
                blocE_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocE_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocE_anger_vid2 = 1
            else:
                blocE_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocE_disgust_vid1 = 1
            if len(disgust) == 2:
                blocE_disgust_vid2 = 1
            else:
                blocE_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocE_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocE_disgust_vid2 = 1
            else:
                blocE_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocE_fear_vid1 = 1
            if len(fear) == 2:
                blocE_fear_vid2 = 1
            else:
                blocE_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocE_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocE_fear_vid2 = 1
            else:
                blocE_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocE_happiness_vid1 = 1
            if len(happiness) == 2:
                blocE_happiness_vid2 = 1
            else:
                blocE_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocE_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocE_happiness_vid2 = 1
            else:
                blocE_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocE_sadness_vid1 = 1
            if len(sadness) == 2:
                blocE_sadness_vid2 = 1
            else:
                blocE_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocE_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocE_sadness_vid2 = 1
            else:
                blocE_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocE_surprise_vid1 = 1
            if len(surprise) == 2:
                blocE_surprise_vid2 = 1
            else:
                blocE_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocE_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocE_surprise_vid2 = 1
            else:
                blocE_surprise_vid2 = 0
        
        '''Add Bloc E data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocE_title_vid1)
        sentimentList.append(blocE_sent_vid1)
        activationList.append(blocE_act_vid1)
        angerList.append(blocE_anger_vid1)
        disgustList.append(blocE_disgust_vid1)
        fearList.append(blocE_fear_vid1)
        happinessList.append(blocE_happiness_vid1)
        sadnessList.append(blocE_sadness_vid1)
        surpriseList.append(blocE_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocE_title_vid2)
        sentimentList.append(blocE_sent_vid2)
        activationList.append(blocE_act_vid2)
        angerList.append(blocE_anger_vid2)
        disgustList.append(blocE_disgust_vid2)
        fearList.append(blocE_fear_vid2)
        happinessList.append(blocE_happiness_vid2)
        sadnessList.append(blocE_sadness_vid2)
        surpriseList.append(blocE_surprise_vid2)

        #-----------------
        # BlocF
        #-----------------
        '''count n of bars, which separate variables'''
        numBars = qualtricsRaw['BL_cNiU4FegXk1GkCx_DO'][i].count('|') #count seperators (|)       
        '''break strings into components, which are separated by bars'''
        blocF_DO = findStringParts(qualtricsRaw['BL_cNiU4FegXk1GkCx_DO'][i], '|', numBars) 
        blocF_title_vid1 = blocF_DO[0] # The first video title
        blocF_title_vid2 = blocF_DO[1] # The second video title
        '''arousal code for first video'''
        blocF_act_vid1 = qualtricsRaw['QID1063_1'][i] 
        '''arousal code for second video'''
        blocF_act_vid2 = qualtricsRaw['QID1063_2'][i] 
        '''sentiment code for first video'''
        blocF_sent_vid1 = qualtricsRaw['QID1064_1'][i] 
        '''sentiment code for second video'''
        blocF_sent_vid2 = qualtricsRaw['QID1064_2'][i] 
        
        '''List of videos where specific emotions are indicated'''
        anger = findStringParts(qualtricsRaw['QID1065#1_1'][i],',',2)
        disgust = findStringParts(qualtricsRaw['QID1065#1_2'][i],',',2)
        fear = findStringParts(qualtricsRaw['QID1065#1_3'][i],',',2)
        happiness = findStringParts(qualtricsRaw['QID1065#1_4'][i], ',',2)
        sadness = findStringParts(qualtricsRaw['QID1065#1_5'][i],',',2)
        surprise = findStringParts(qualtricsRaw['QID1065#1_6'][i],',',2)                                       
        
        '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
        if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
        1 is not listed first, check to see if Video 2 is listed first, and 
        score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
        '''Anger'''
        if anger[0] == "Video 1":  
            blocF_anger_vid1 = 1
            if len(anger)== 2:
                blocF_anger_vid2 = 1
            else:
                blocF_anger_vid2 = 0 
        elif anger[0] != "Video 1":
            blocF_anger_vid1 = 0
            if anger[0] == "Video 2":
                blocF_anger_vid2 = 1
            else:
                blocF_anger_vid2 = 0
        '''Disgust'''
        if disgust[0] == "Video 1":  
            blocF_disgust_vid1 = 1
            if len(disgust) == 2:
                blocF_disgust_vid2 = 1
            else:
                blocF_disgust_vid2 = 0 
        elif disgust[0] != "Video 1":
            blocF_disgust_vid1 = 0
            if disgust[0] == "Video 2":
                blocF_disgust_vid2 = 1
            else:
                blocF_disgust_vid2 = 0
        '''Fear'''
        if fear[0] == "Video 1":  
            blocF_fear_vid1 = 1
            if len(fear) == 2:
                blocF_fear_vid2 = 1
            else:
                blocF_fear_vid2 = 0 
        elif fear[0] != "Video 1":
            blocF_fear_vid1 = 0
            if fear[0] == "Video 2":
                blocF_fear_vid2 = 1
            else:
                blocF_fear_vid2 = 0
        '''Happiness'''
        if happiness[0] == "Video 1":  
            blocF_happiness_vid1 = 1
            if len(happiness) == 2:
                blocF_happiness_vid2 = 1
            else:
                blocF_happiness_vid2 = 0 
        if happiness[0] != "Video 1":
            blocF_happiness_vid1 = 0
            if happiness[0] == "Video 2":
                blocF_happiness_vid2 = 1
            else:
                blocF_happiness_vid2 = 0
        '''Sadness'''
        if sadness[0] == "Video 1":  
            blocF_sadness_vid1 = 1
            if len(sadness) == 2:
                blocF_sadness_vid2 = 1
            else:
                blocF_sadness_vid2 = 0 
        elif sadness[0] != "Video 1":
            blocF_sadness_vid1 = 0
            if sadness[0] == "Video 2":
                blocF_sadness_vid2 = 1
            else:
                blocF_sadness_vid2 = 0
        '''Surprise'''
        if surprise[0] == "Video 1":  
            blocF_surprise_vid1 = 1
            if len(surprise) == 2:
                blocF_surprise_vid2 = 1
            else:
                blocF_surprise_vid2 = 0 
        elif surprise[0] != "Video 1":
            blocF_surprise_vid1 = 0
            if surprise[0] == "Video 2":
                blocF_surprise_vid2 = 1
            else:
                blocF_surprise_vid2 = 0
        
        '''Add Bloc F data to running Tally'''
        '''For Video 1'''
        coderList.append(coder)
        videoList.append(blocF_title_vid1)
        sentimentList.append(blocF_sent_vid1)
        activationList.append(blocF_act_vid1)
        angerList.append(blocF_anger_vid1)
        disgustList.append(blocF_disgust_vid1)
        fearList.append(blocF_fear_vid1)
        happinessList.append(blocF_happiness_vid1)
        sadnessList.append(blocF_sadness_vid1)
        surpriseList.append(blocF_surprise_vid1)
        '''For Video 2'''
        coderList.append(coder)
        videoList.append(blocF_title_vid2)
        sentimentList.append(blocF_sent_vid2)
        activationList.append(blocF_act_vid2)
        angerList.append(blocF_anger_vid2)
        disgustList.append(blocF_disgust_vid2)
        fearList.append(blocF_fear_vid2)
        happinessList.append(blocF_happiness_vid2)
        sadnessList.append(blocF_sadness_vid2)
        surpriseList.append(blocF_surprise_vid2)

        #-----------------
        # BlocA1B1
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_0uhk6r0UWlNJ3tb_DO'][i]):
            numBars = str(qualtricsRaw['BL_0uhk6r0UWlNJ3tb_DO'][i]).count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA1B1_DO = findStringParts(qualtricsRaw['BL_0uhk6r0UWlNJ3tb_DO'][i], '|', numBars) 
            blocA1B1_title_vid1 = blocA1B1_DO[0] # The first video title
            blocA1B1_title_vid2 = blocA1B1_DO[1] # The second video title
            '''arousal code for first video'''
            blocA1B1_act_vid1 = qualtricsRaw['QID4911_1'][i] 
            '''arousal code for second video'''
            blocA1B1_act_vid2 = qualtricsRaw['QID4911_2'][i] 
            '''sentiment code for first video'''
            blocA1B1_sent_vid1 = qualtricsRaw['QID4910_1'][i] 
            '''sentiment code for second video'''
            blocA1B1_sent_vid2 = qualtricsRaw['QID4910_2'][i] 
        
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID4912#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID4912#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID4912#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID4912#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID4912#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID4912#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA1B1_anger_vid1 = 1
                if len(anger)== 2:
                    blocA1B1_anger_vid2 = 1
                else:
                    blocA1B1_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA1B1_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA1B1_anger_vid2 = 1
                else:
                    blocA1B1_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA1B1_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA1B1_disgust_vid2 = 1
                else:
                    blocA1B1_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA1B1_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA1B1_disgust_vid2 = 1
                else:
                    blocA1B1_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA1B1_fear_vid1 = 1
                if len(fear) == 2:
                    blocA1B1_fear_vid2 = 1
                else:
                    blocA1B1_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA1B1_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA1B1_fear_vid2 = 1
                else:
                    blocA1B1_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA1B1_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA1B1_happiness_vid2 = 1
                else:
                    blocA1B1_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA1B1_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA1B1_happiness_vid2 = 1
                else:
                    blocA1B1_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA1B1_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA1B1_sadness_vid2 = 1
                else:
                    blocA1B1_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA1B1_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA1B1_sadness_vid2 = 1
                else:
                    blocA1B1_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA1B1_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA1B1_surprise_vid2 = 1
                else:
                    blocA1B1_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA1B1_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA1B1_surprise_vid2 = 1
                else:
                    blocA1B1_surprise_vid2 = 0
            
            '''Add Bloc A1B1 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA1B1_title_vid1)
            sentimentList.append(blocA1B1_sent_vid1)
            activationList.append(blocA1B1_act_vid1)
            angerList.append(blocA1B1_anger_vid1)
            disgustList.append(blocA1B1_disgust_vid1)
            fearList.append(blocA1B1_fear_vid1)
            happinessList.append(blocA1B1_happiness_vid1)
            sadnessList.append(blocA1B1_sadness_vid1)
            surpriseList.append(blocA1B1_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA1B1_title_vid2)
            sentimentList.append(blocA1B1_sent_vid2)
            activationList.append(blocA1B1_act_vid2)
            angerList.append(blocA1B1_anger_vid2)
            disgustList.append(blocA1B1_disgust_vid2)
            fearList.append(blocA1B1_fear_vid2)
            happinessList.append(blocA1B1_happiness_vid2)
            sadnessList.append(blocA1B1_sadness_vid2)
            surpriseList.append(blocA1B1_surprise_vid2)


        #-----------------
        # BlocA1B2
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_eCHbbimkb0dc5i5_DO'][i]):
            numBars = str(qualtricsRaw['BL_eCHbbimkb0dc5i5_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_eCHbbimkb0dc5i5_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA1B2_DO = findStringParts(qualtricsRaw['BL_eCHbbimkb0dc5i5_DO'][i], '|', numBars) 
            blocA1B2_title_vid1 = blocA1B2_DO[0] # The first video title
            blocA1B2_title_vid2 = blocA1B2_DO[1] # The second video title
            '''arousal code for first video'''
            blocA1B2_act_vid1 = qualtricsRaw['QID5054_1'][i] 
            '''arousal code for second video'''
            blocA1B2_act_vid2 = qualtricsRaw['QID5054_2'][i] 
            '''sentiment code for first video'''
            blocA1B2_sent_vid1 = qualtricsRaw['QID5052_1'][i] 
            '''sentiment code for second video'''
            blocA1B2_sent_vid2 = qualtricsRaw['QID5052_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5056#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5056#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5056#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5056#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5056#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5056#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA1B2_anger_vid1 = 1
                if len(anger)== 2:
                    blocA1B2_anger_vid2 = 1
                else:
                    blocA1B2_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA1B2_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA1B2_anger_vid2 = 1
                else:
                    blocA1B2_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA1B2_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA1B2_disgust_vid2 = 1
                else:
                    blocA1B2_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA1B2_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA1B2_disgust_vid2 = 1
                else:
                    blocA1B2_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA1B2_fear_vid1 = 1
                if len(fear) == 2:
                    blocA1B2_fear_vid2 = 1
                else:
                    blocA1B2_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA1B2_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA1B2_fear_vid2 = 1
                else:
                    blocA1B2_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA1B2_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA1B2_happiness_vid2 = 1
                else:
                    blocA1B2_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA1B2_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA1B2_happiness_vid2 = 1
                else:
                    blocA1B2_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA1B2_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA1B2_sadness_vid2 = 1
                else:
                    blocA1B2_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA1B2_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA1B2_sadness_vid2 = 1
                else:
                    blocA1B2_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA1B2_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA1B2_surprise_vid2 = 1
                else:
                    blocA1B2_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA1B2_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA1B2_surprise_vid2 = 1
                else:
                    blocA1B2_surprise_vid2 = 0
            
            '''Add Bloc A1B2 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA1B2_title_vid1)
            sentimentList.append(blocA1B2_sent_vid1)
            activationList.append(blocA1B2_act_vid1)
            angerList.append(blocA1B2_anger_vid1)
            disgustList.append(blocA1B2_disgust_vid1)
            fearList.append(blocA1B2_fear_vid1)
            happinessList.append(blocA1B2_happiness_vid1)
            sadnessList.append(blocA1B2_sadness_vid1)
            surpriseList.append(blocA1B2_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA1B2_title_vid2)
            sentimentList.append(blocA1B2_sent_vid2)
            activationList.append(blocA1B2_act_vid2)
            angerList.append(blocA1B2_anger_vid2)
            disgustList.append(blocA1B2_disgust_vid2)
            fearList.append(blocA1B2_fear_vid2)
            happinessList.append(blocA1B2_happiness_vid2)
            sadnessList.append(blocA1B2_sadness_vid2)
            surpriseList.append(blocA1B2_surprise_vid2)

       #-----------------
        # BlocA1F1
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_0kXaBSNouGm7OXH_DO'][i]):
            numBars = str(qualtricsRaw['BL_0kXaBSNouGm7OXH_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_0kXaBSNouGm7OXH_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA1F1_DO = findStringParts(qualtricsRaw['BL_0kXaBSNouGm7OXH_DO'][i], '|', numBars) 
            blocA1F1_title_vid1 = blocA1F1_DO[0] # The first video title
            blocA1F1_title_vid2 = blocA1F1_DO[1] # The second video title
            '''arousal code for first video'''
            blocA1F1_act_vid1 = qualtricsRaw['QID5342_1'][i] 
            '''arousal code for second video'''
            blocA1F1_act_vid2 = qualtricsRaw['QID5342_2'][i] 
            '''sentiment code for first video'''
            blocA1F1_sent_vid1 = qualtricsRaw['QID5341_1'][i] 
            '''sentiment code for second video'''
            blocA1F1_sent_vid2 = qualtricsRaw['QID5341_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5343#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5343#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5343#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5343#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5343#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5343#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA1F1_anger_vid1 = 1
                if len(anger)== 2:
                    blocA1F1_anger_vid2 = 1
                else:
                    blocA1F1_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA1F1_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA1F1_anger_vid2 = 1
                else:
                    blocA1F1_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA1F1_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA1F1_disgust_vid2 = 1
                else:
                    blocA1F1_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA1F1_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA1F1_disgust_vid2 = 1
                else:
                    blocA1F1_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA1F1_fear_vid1 = 1
                if len(fear) == 2:
                    blocA1F1_fear_vid2 = 1
                else:
                    blocA1F1_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA1F1_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA1F1_fear_vid2 = 1
                else:
                    blocA1F1_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA1F1_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA1F1_happiness_vid2 = 1
                else:
                    blocA1F1_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA1F1_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA1F1_happiness_vid2 = 1
                else:
                    blocA1F1_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA1F1_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA1F1_sadness_vid2 = 1
                else:
                    blocA1F1_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA1F1_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA1F1_sadness_vid2 = 1
                else:
                    blocA1F1_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA1F1_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA1F1_surprise_vid2 = 1
                else:
                    blocA1F1_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA1F1_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA1F1_surprise_vid2 = 1
                else:
                    blocA1F1_surprise_vid2 = 0
            
            '''Add Bloc A1F1 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA1F1_title_vid1)
            sentimentList.append(blocA1F1_sent_vid1)
            activationList.append(blocA1F1_act_vid1)
            angerList.append(blocA1F1_anger_vid1)
            disgustList.append(blocA1F1_disgust_vid1)
            fearList.append(blocA1F1_fear_vid1)
            happinessList.append(blocA1F1_happiness_vid1)
            sadnessList.append(blocA1F1_sadness_vid1)
            surpriseList.append(blocA1F1_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA1F1_title_vid2)
            sentimentList.append(blocA1F1_sent_vid2)
            activationList.append(blocA1F1_act_vid2)
            angerList.append(blocA1F1_anger_vid2)
            disgustList.append(blocA1F1_disgust_vid2)
            fearList.append(blocA1F1_fear_vid2)
            happinessList.append(blocA1F1_happiness_vid2)
            sadnessList.append(blocA1F1_sadness_vid2)
            surpriseList.append(blocA1F1_surprise_vid2)

       #-----------------
        # BlocA1F2
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_0kTwd0XKn0tOQ7z_DO'][i]):
            numBars = str(qualtricsRaw['BL_0kTwd0XKn0tOQ7z_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_0kTwd0XKn0tOQ7z_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA1F2_DO = findStringParts(qualtricsRaw['BL_0kTwd0XKn0tOQ7z_DO'][i], '|', numBars) 
            blocA1F2_title_vid1 = blocA1F2_DO[0] # The first video title
            blocA1F2_title_vid2 = blocA1F2_DO[1] # The second video title
            '''arousal code for first video'''
            blocA1F2_act_vid1 = qualtricsRaw['QID5520_1'][i] 
            '''arousal code for second video'''
            blocA1F2_act_vid2 = qualtricsRaw['QID5520_2'][i] 
            '''sentiment code for first video'''
            blocA1F2_sent_vid1 = qualtricsRaw['QID5522_1'][i] 
            '''sentiment code for second video'''
            blocA1F2_sent_vid2 = qualtricsRaw['QID5522_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5521#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5521#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5521#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5521#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5521#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5521#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA1F2_anger_vid1 = 1
                if len(anger)== 2:
                    blocA1F2_anger_vid2 = 1
                else:
                    blocA1F2_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA1F2_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA1F2_anger_vid2 = 1
                else:
                    blocA1F2_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA1F2_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA1F2_disgust_vid2 = 1
                else:
                    blocA1F2_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA1F2_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA1F2_disgust_vid2 = 1
                else:
                    blocA1F2_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA1F2_fear_vid1 = 1
                if len(fear) == 2:
                    blocA1F2_fear_vid2 = 1
                else:
                    blocA1F2_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA1F2_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA1F2_fear_vid2 = 1
                else:
                    blocA1F2_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA1F2_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA1F2_happiness_vid2 = 1
                else:
                    blocA1F2_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA1F2_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA1F2_happiness_vid2 = 1
                else:
                    blocA1F2_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA1F2_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA1F2_sadness_vid2 = 1
                else:
                    blocA1F2_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA1F2_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA1F2_sadness_vid2 = 1
                else:
                    blocA1F2_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA1F2_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA1F2_surprise_vid2 = 1
                else:
                    blocA1F2_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA1F2_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA1F2_surprise_vid2 = 1
                else:
                    blocA1F2_surprise_vid2 = 0
            
            '''Add Bloc A1F2 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA1F2_title_vid1)
            sentimentList.append(blocA1F2_sent_vid1)
            activationList.append(blocA1F2_act_vid1)
            angerList.append(blocA1F2_anger_vid1)
            disgustList.append(blocA1F2_disgust_vid1)
            fearList.append(blocA1F2_fear_vid1)
            happinessList.append(blocA1F2_happiness_vid1)
            sadnessList.append(blocA1F2_sadness_vid1)
            surpriseList.append(blocA1F2_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA1F2_title_vid2)
            sentimentList.append(blocA1F2_sent_vid2)
            activationList.append(blocA1F2_act_vid2)
            angerList.append(blocA1F2_anger_vid2)
            disgustList.append(blocA1F2_disgust_vid2)
            fearList.append(blocA1F2_fear_vid2)
            happinessList.append(blocA1F2_happiness_vid2)
            surpriseList.append(blocA1F2_surprise_vid2)



        #-----------------
        # BlocA2F1
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_8expPTVNXuTVOUB_DO'][i]):
            numBars = str(qualtricsRaw['BL_8expPTVNXuTVOUB_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_8expPTVNXuTVOUB_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA2F1_DO = findStringParts(qualtricsRaw['BL_8expPTVNXuTVOUB_DO'][i], '|', numBars) 
            blocA2F1_title_vid1 = blocA2F1_DO[0] # The first video title
            blocA2F1_title_vid2 = blocA2F1_DO[1] # The second video title
            '''arousal code for first video'''
            blocA2F1_act_vid1 = qualtricsRaw['QID5693_1'][i] 
            '''arousal code for second video'''
            blocA2F1_act_vid2 = qualtricsRaw['QID5693_2'][i] 
            '''sentiment code for first video'''
            blocA2F1_sent_vid1 = qualtricsRaw['QID5695_1'][i] 
            '''sentiment code for second video'''
            blocA2F1_sent_vid2 = qualtricsRaw['QID5695_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5694#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5694#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5694#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5694#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5694#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5694#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA2F1_anger_vid1 = 1
                if len(anger)== 2:
                    blocA2F1_anger_vid2 = 1
                else:
                    blocA2F1_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA2F1_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA2F1_anger_vid2 = 1
                else:
                    blocA2F1_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA2F1_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA2F1_disgust_vid2 = 1
                else:
                    blocA2F1_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA2F1_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA2F1_disgust_vid2 = 1
                else:
                    blocA2F1_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA2F1_fear_vid1 = 1
                if len(fear) == 2:
                    blocA2F1_fear_vid2 = 1
                else:
                    blocA2F1_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA2F1_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA2F1_fear_vid2 = 1
                else:
                    blocA2F1_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA2F1_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA2F1_happiness_vid2 = 1
                else:
                    blocA2F1_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA2F1_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA2F1_happiness_vid2 = 1
                else:
                    blocA2F1_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA2F1_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA2F1_sadness_vid2 = 1
                else:
                    blocA2F1_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA2F1_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA2F1_sadness_vid2 = 1
                else:
                    blocA2F1_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA2F1_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA2F1_surprise_vid2 = 1
                else:
                    blocA2F1_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA2F1_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA2F1_surprise_vid2 = 1
                else:
                    blocA2F1_surprise_vid2 = 0
            
            '''Add Bloc A2F1 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA2F1_title_vid1)
            sentimentList.append(blocA2F1_sent_vid1)
            activationList.append(blocA2F1_act_vid1)
            angerList.append(blocA2F1_anger_vid1)
            disgustList.append(blocA2F1_disgust_vid1)
            fearList.append(blocA2F1_fear_vid1)
            happinessList.append(blocA2F1_happiness_vid1)
            sadnessList.append(blocA2F1_sadness_vid1)
            surpriseList.append(blocA2F1_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA2F1_title_vid2)
            sentimentList.append(blocA2F1_sent_vid2)
            activationList.append(blocA2F1_act_vid2)
            angerList.append(blocA2F1_anger_vid2)
            disgustList.append(blocA2F1_disgust_vid2)
            fearList.append(blocA2F1_fear_vid2)
            happinessList.append(blocA2F1_happiness_vid2)
            sadnessList.append(blocA2F1_sadness_vid2)
            surpriseList.append(blocA2F1_surprise_vid2)


        #-----------------
        # BlocA2B1
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_6tBHFflywlCq6nb_DO'][i]):
            numBars = str(qualtricsRaw['BL_6tBHFflywlCq6nb_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_6tBHFflywlCq6nb_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA2B1_DO = findStringParts(qualtricsRaw['BL_6tBHFflywlCq6nb_DO'][i], '|', numBars) 
            blocA2B1_title_vid1 = blocA2B1_DO[0] # The first video title
            blocA2B1_title_vid2 = blocA2B1_DO[1] # The second video title
            '''arousal code for first video'''
            blocA2B1_act_vid1 = qualtricsRaw['QID5781_1'][i] 
            '''arousal code for second video'''
            blocA2B1_act_vid2 = qualtricsRaw['QID5781_2'][i] 
            '''sentiment code for first video'''
            blocA2B1_sent_vid1 = qualtricsRaw['QID5782_1'][i] 
            '''sentiment code for second video'''
            blocA2B1_sent_vid2 = qualtricsRaw['QID5782_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5783#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5783#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5783#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5783#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5783#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5783#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA2B1_anger_vid1 = 1
                if len(anger)== 2:
                    blocA2B1_anger_vid2 = 1
                else:
                    blocA2B1_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA2B1_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA2B1_anger_vid2 = 1
                else:
                    blocA2B1_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA2B1_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA2B1_disgust_vid2 = 1
                else:
                    blocA2B1_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA2B1_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA2B1_disgust_vid2 = 1
                else:
                    blocA2B1_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA2B1_fear_vid1 = 1
                if len(fear) == 2:
                    blocA2B1_fear_vid2 = 1
                else:
                    blocA2B1_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA2B1_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA2B1_fear_vid2 = 1
                else:
                    blocA2B1_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA2B1_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA2B1_happiness_vid2 = 1
                else:
                    blocA2B1_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA2B1_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA2B1_happiness_vid2 = 1
                else:
                    blocA2B1_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA2B1_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA2B1_sadness_vid2 = 1
                else:
                    blocA2B1_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA2B1_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA2B1_sadness_vid2 = 1
                else:
                    blocA2B1_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA2B1_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA2B1_surprise_vid2 = 1
                else:
                    blocA2B1_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA2B1_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA2B1_surprise_vid2 = 1
                else:
                    blocA2B1_surprise_vid2 = 0
            
            '''Add Bloc A2B1 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA2B1_title_vid1)
            sentimentList.append(blocA2B1_sent_vid1)
            activationList.append(blocA2B1_act_vid1)
            angerList.append(blocA2B1_anger_vid1)
            disgustList.append(blocA2B1_disgust_vid1)
            fearList.append(blocA2B1_fear_vid1)
            happinessList.append(blocA2B1_happiness_vid1)
            sadnessList.append(blocA2B1_sadness_vid1)
            surpriseList.append(blocA2B1_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA2B1_title_vid2)
            sentimentList.append(blocA2B1_sent_vid2)
            activationList.append(blocA2B1_act_vid2)
            angerList.append(blocA2B1_anger_vid2)
            disgustList.append(blocA2B1_disgust_vid2)
            fearList.append(blocA2B1_fear_vid2)
            happinessList.append(blocA2B1_happiness_vid2)
            sadnessList.append(blocA2B1_sadness_vid2)
            surpriseList.append(blocA2B1_surprise_vid2)
        
        #-----------------
        # BlocA2B2
        #-----------------
        '''count n of bars, which separate variables'''
        if not str(qualtricsRaw['BL_42F6yra3ogqCtpP_DO'][i]):
            numBars = str(qualtricsRaw['BL_42F6yra3ogqCtpP_DO'][i]).count('|') #count seperators (|)
            '''count n of bars, which separate variables'''
            numBars = qualtricsRaw['BL_42F6yra3ogqCtpP_DO'][i].count('|') #count seperators (|)       
            '''break strings into components, which are separated by bars'''
            blocA2B2_DO = findStringParts(qualtricsRaw['BL_42F6yra3ogqCtpP_DO'][i], '|', numBars) 
            blocA2B2_title_vid1 = blocA2B2_DO[0] # The first video title
            blocA2B2_title_vid2 = blocA2B2_DO[1] # The second video title
            '''arousal code for first video'''
            blocA2B2_act_vid1 = qualtricsRaw['QID5954_1'][i] 
            '''arousal code for second video'''
            blocA2B2_act_vid2 = qualtricsRaw['QID5954_2'][i] 
            '''sentiment code for first video'''
            blocA2B2_sent_vid1 = qualtricsRaw['QID5955_1'][i] 
            '''sentiment code for second video'''
            blocA2B2_sent_vid2 = qualtricsRaw['QID5955_2'][i] 
            
            '''List of videos where specific emotions are indicated'''
            anger = findStringParts(qualtricsRaw['QID5956#1_1'][i],',',2)
            disgust = findStringParts(qualtricsRaw['QID5956#1_2'][i],',',2)
            fear = findStringParts(qualtricsRaw['QID5956#1_3'][i],',',2)
            happiness = findStringParts(qualtricsRaw['QID5956#1_4'][i], ',',2)
            sadness = findStringParts(qualtricsRaw['QID5956#1_5'][i],',',2)
            surprise = findStringParts(qualtricsRaw['QID5956#1_6'][i],',',2)                                       
            
            '''Loop Logic: If video 1 is listed first score 1 for video 1 and check 
            if video 2 is listed second (score 1 if it is, 0 otherwise.) If video
            1 is not listed first, check to see if Video 2 is listed first, and 
            score 1 if it is, and 0 otherwise.  Repeat for each emotion.'''
            '''Anger'''
            if anger[0] == "Video 1":  
                blocA2B2_anger_vid1 = 1
                if len(anger)== 2:
                    blocA2B2_anger_vid2 = 1
                else:
                    blocA2B2_anger_vid2 = 0 
            elif anger[0] != "Video 1":
                blocA2B2_anger_vid1 = 0
                if anger[0] == "Video 2":
                    blocA2B2_anger_vid2 = 1
                else:
                    blocA2B2_anger_vid2 = 0
            '''Disgust'''
            if disgust[0] == "Video 1":  
                blocA2B2_disgust_vid1 = 1
                if len(disgust) == 2:
                    blocA2B2_disgust_vid2 = 1
                else:
                    blocA2B2_disgust_vid2 = 0 
            elif disgust[0] != "Video 1":
                blocA2B2_disgust_vid1 = 0
                if disgust[0] == "Video 2":
                    blocA2B2_disgust_vid2 = 1
                else:
                    blocA2B2_disgust_vid2 = 0
            '''Fear'''
            if fear[0] == "Video 1":  
                blocA2B2_fear_vid1 = 1
                if len(fear) == 2:
                    blocA2B2_fear_vid2 = 1
                else:
                    blocA2B2_fear_vid2 = 0 
            elif fear[0] != "Video 1":
                blocA2B2_fear_vid1 = 0
                if fear[0] == "Video 2":
                    blocA2B2_fear_vid2 = 1
                else:
                    blocA2B2_fear_vid2 = 0
            '''Happiness'''
            if happiness[0] == "Video 1":  
                blocA2B2_happiness_vid1 = 1
                if len(happiness) == 2:
                    blocA2B2_happiness_vid2 = 1
                else:
                    blocA2B2_happiness_vid2 = 0 
            if happiness[0] != "Video 1":
                blocA2B2_happiness_vid1 = 0
                if happiness[0] == "Video 2":
                    blocA2B2_happiness_vid2 = 1
                else:
                    blocA2B2_happiness_vid2 = 0
            '''Sadness'''
            if sadness[0] == "Video 1":  
                blocA2B2_sadness_vid1 = 1
                if len(sadness) == 2:
                    blocA2B2_sadness_vid2 = 1
                else:
                    blocA2B2_sadness_vid2 = 0 
            elif sadness[0] != "Video 1":
                blocA2B2_sadness_vid1 = 0
                if sadness[0] == "Video 2":
                    blocA2B2_sadness_vid2 = 1
                else:
                    blocA2B2_sadness_vid2 = 0
            '''Surprise'''
            if surprise[0] == "Video 1":  
                blocA2B2_surprise_vid1 = 1
                if len(surprise) == 2:
                    blocA2B2_surprise_vid2 = 1
                else:
                    blocA2B2_surprise_vid2 = 0 
            elif surprise[0] != "Video 1":
                blocA2B2_surprise_vid1 = 0
                if surprise[0] == "Video 2":
                    blocA2B2_surprise_vid2 = 1
                else:
                    blocA2B2_surprise_vid2 = 0
            
            '''Add Bloc A2B2 data to running Tally'''
            '''For Video 1'''
            coderList.append(coder)
            videoList.append(blocA2B2_title_vid1)
            sentimentList.append(blocA2B2_sent_vid1)
            activationList.append(blocA2B2_act_vid1)
            angerList.append(blocA2B2_anger_vid1)
            disgustList.append(blocA2B2_disgust_vid1)
            fearList.append(blocA2B2_fear_vid1)
            happinessList.append(blocA2B2_happiness_vid1)
            sadnessList.append(blocA2B2_sadness_vid1)
            surpriseList.append(blocA2B2_surprise_vid1)
            '''For Video 2'''
            coderList.append(coder)
            videoList.append(blocA2B2_title_vid2)
            sentimentList.append(blocA2B2_sent_vid2)
            activationList.append(blocA2B2_act_vid2)
            angerList.append(blocA2B2_anger_vid2)
            disgustList.append(blocA2B2_disgust_vid2)
            fearList.append(blocA2B2_fear_vid2)        
            happinessList.append(blocA2B2_happiness_vid2)
            sadnessList.append(blocA2B2_sadness_vid2)
            surpriseList.append(blocA2B2_surprise_vid2)

#-----------------------------------------------------------------------------
# Save Structured Data
#-----------------------------------------------------------------------------

print(len(coderList))
print(len(videoList))
print(len(sentimentList))
print(len(activationList))
print(len(angerList))
print(len(disgustList))
print(len(fearList))
print(len(happinessList))
print(len(sadnessList))
print(len(surpriseList))
print(surpriseList)

'''Combine Running Tally Lists in Dictionary'''
qualtricsStructured = {'Coder': coderList,
                       'Video': videoList,
                       'Sentiment': sentimentList,
                       'Activation': activationList,
                       'Anger': angerList,
                       'Disgust': disgustList,
                       'Fear': fearList,
                       'Happiness': happinessList,
                       'Sadness': sadnessList,
                       'Surprise': surpriseList}

'''Convert to Pandas DF'''
qualtricsStructured = pd.DataFrame(qualtricsStructured)

'''Assign Missing Values'''
qualtricsStructured = qualtricsStructured.replace('-99',pd.NaT)

'''Drop Missing Values, as there was no reason for coders to produce them
and only one coder did, as if he was repeatedly interrupted in the middle
of coding a single video.  This could have been a connection issue.'''

qualtricsStructured = qualtricsStructured.dropna()


'''Export to CSV'''
qualtricsStructured.to_csv('qualtricsStructured.csv', encoding='utf-8')


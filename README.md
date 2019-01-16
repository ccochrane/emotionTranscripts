# emotionParliament
The Automated Detection of Emotion in Transcripts of Parliamentary Speech: Comparing Human and Machine Classification of the Video and Written Records of Debates in the Canadian House of Commons

Abstract: The volume of machine-readable text communication about politics has increased exponentially over the past three decades, spawning the pursuit of new tools for automated analyses of sentiment in large political corpora.  Unlike written communication, however, the expression of emotion in speech is not confined to word-choice and syntax, and instead relies heavily on intonation, facial expressions, and body language, which go undetected in analyses of political text.  This raises the question of whether tools developed for analyses of writing can detect sentiment in transcripts of political speech.  In this paper, we survey a variety of strategies for the automated analysis of emotion in text, and test their outputs against human-coded sentiment analysis of the written and video record of debates in the Canadian House of Commons. We find that transcripts capture the valence, but not the emotional intensity, of political speeches. We also find that while leading dictionary and supervised approaches to sentiment detection performed reasonably well, using domain specific word embeddings induced from state-of-the-art Neural Networks surpassed these other approaches, and achieved near-human level performance. 

(1) selectionScript.R - A script for selecting video clips to extract from CPAC Question Periods.

(2) extractedVideoTranscripts.csv - The list of videos extracted from Step 1, along with date, speaker, party, language of speech, Hansard record (English), timeStamp (MM:SS), sentence length (SS:MS), and video link (youTube). 

(3) videoCodingInstrument.pdf - An image of the Qualtrics coding instrument for the video clips.

(4) emotionInHansard_December+20%2C+2018_14.52.csv - The raw output from the Qualtrics survey instrument that the Video Coders used to code the videos.

(5) qualtricsDataExtract.py - A script for structuring the raw Qualtrics output (from Step 4).  

(6) qualtricsStructured.csv - The structured Qualtrics data (from Step 5).

(7) createVideoCoderRecord.py - A script for extracting (from Step 6) the first two coding decisions of each video coder for each video.

(8) videoCoderAverages.csv - The record of video coding decisions (from Step 7), which captures, for each video coder and video, the first and second score that the coder assigned for activation and sentiment, as well as the averages of their first two scores for both dimensions. Rows are videos.  Columns are: v1Act1, v1Act2, v1ActAvg, v1Sent1, v1Sent2, v1SentAvg, v2Act1 ... v3SentAct. 

(9) The csv files of the text coding, as returned by the text coders for rounds 1 and 2.  These files are:
                a) cm_coding1.csv & cm_coding2.csv for coder CM
                b) sf_coding1.csv & sf_coding2.csv for coder SF
                c) jv_coding1.csv & jv_coding2.csv for coder JV

(10) createTextCoderRecord.py - A script for rearranging and merging the coding data (from Step 9) of the text coders.

(11) textCoderAverages.csv - The record of text coding decisions (from Step 10), which captures, for each text coder and video, the first and second score that the coder assigned for activation and sentiment, as well as the averages of their first two scores for both dimensions. Rows are videos.  Columns are: t1Act1, t1Act2, t1ActAvg, t1Sent1, t1Sent2, t1SentAvg, t2Act1 ... t3SentAct. 

(12) mergeTextVideoCoding.py - A script for merging the video coding data (from Step 8) and the text coding data (from Step 11).

(13) fullCodingData.csv - The merged record of video and text coding decisions (from Step 12).

(14) coderReliability.R - A script for calculating and graphing the intercoder consistency from the coding data (from Step 13) 

(15) coderReliability.PDF - The graph of coder reliability coefficients (from Step 14).

(16) /Hansard - The files for Hansard stored in the contemporary .xml format, which extends back to the 39th (2006) Parliament.  Scraped from www.ourcommons.ca.

(17) createAuthorityFile.xlsx - An excel file that links the quasi-sporadic numerical MP codes used in the Hansard .xml files (from Step 16) with their actual names and biographical information (sex, visibleMinority, indigenous, date of birth, province of birth, country of birth, date elected, province of district, and the link to their full bio on the Parlinfo site). This file also generates script for storing spreadsheet data entry as a python dictionary file.

(18) createAuthorityFile.py - The script produced from Step 17 for creating the authorityFile as a python dictionary file and then pickling it.  

(19) authorityFile.p - the pickled authorityFile in python dictionary format (from Step 18).

(20) hansardParser.py - [Requires Windows] A script for parsing the .xml schema used in the Hansard files (from Step 16) at the speech level, linking each speech to its speaker and the speaker's bio (from Step 19), and storing the results in a CSV file (which can be imported into 64-bit Excel via Data Import, but not properly opened in Excel without using data import). Available at https://www.dropbox.com/s/4xzw3rscu7x7xn3/hansardExtractedSpeechesFull.csv.zip?dl=0 (hansardExtractedSpeechesFull.csv, compressed to ~375MB, tab separated). Requires Windows b/c Pandas not cooperating with Mac handling of the large CSV file.  

(21) word2vecTrain.py - [Requires Windows] A script for training a word2vec model on the parsed speeches from Hansard (from Step 20).

(22) word2vecRun.py - [Requires Windows] A script for running the w2v model trained on Hansard (from Step 21) and applying it to the Hansard transcripts of the video snippets (from Step 2).  

(23) w2vScores.csv - A csv file linking the transcripts of the video snippets (from Step 2) to the sentiment scores generated
using the word2vec model (from Step 22).  

(24) applySentimentR.R - A script for applying popular sentiment dictionaries in R to the extracted Video Transcripts (from Step 2). Dictionaries: Lexicoder, Sentiwordnet, Jockers-Rinker, HuLiu.  

(25) HansardExtractedVideoTranscripts_RSentiment.csv - A csv file of the sentiment scores produced in Step 24. 

(26) applySVMFastTextVader.py - A script that trains Support Vector Machines and FastText on a training subset of the IMDB movie review (https://www.kaggle.com/utathya/imdb-review-dataset) and Stanford handcoded tweet (https://snap.stanford.edu/data/twitter7.html) databases, and applies these models to a testing subset of each corpora. The script applies the models to classify the sentiment of the Hansard transcripts of the video snippets (from Step 2). The  script also scores the sentiment of these snippets using the Valence Aware Dictionary and Sentiment Reasoner (VADER - https://github.com/cjhutto/vaderSentiment) and LIWC (https://liwc.wpengine.com/) sentiment dictionaries. The training data and models are available at https://www.dropbox.com/sh/u91njzwcuvdu8oa/AABkl2vUJRUNEq4WEGSCBql_a?dl=0 (~1.5GB combined).

(27) hansardExtractedVideoTranscripts_SVMFastTextVader.csv - The csv file of the sentiment scores/classifications produced in Step 26.















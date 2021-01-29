# emotionTranscripts
The Automatic Analysis of Emotion in Political Speech Based on Transcripts

Abstract: Automatic sentiment analysis is used extensively in political science. The digitization of legislative transcripts has increased the potential application of established tools for the automated analyses of emotion in text. Unlike in writing, however, expressing emotion in speech involves intonation, facial expressions, and body language. Drawing on a new dataset of annotated texts and videos from the Canadian House of Commons, this paper does three things. First, we examine whether transcripts capture the emotional content of speeches. We find that transcripts capture sentiment, but not emotional arousal. Second, we compare strategies for the automated analysis of sentiment in text. We find that leading approaches performed reasonably well, but sentiment dictionaries generated using word embeddings surpassed these other approaches.  Finally, we test the robustness of the approach based on word embeddings. Although the methodology is reasonably robust to alternative specifications, we find that dictionaries created using word embeddings are sensitive to the choice of seed words and to training corpus size. We conclude by discussing the implications for analyses of political speech.

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

(20) hansardParser.py - [Requires Windows or Linux] A script for parsing the .xml schema used in the Hansard files (from Step 16) at the speech level, linking each speech to its speaker and the speaker's bio (from Step 19), and storing the results in a CSV file (which can be imported into 64-bit Excel via Data Import, but not properly opened in Excel without using data import). Available at https://www.dropbox.com/s/4xzw3rscu7x7xn3/hansardExtractedSpeechesFull.csv.zip?dl=0 (hansardExtractedSpeechesFull.csv, compressed to ~375MB, tab separated). Requires Windows or Linux b/c Pandas not cooperating with Mac handling of the large CSV file.  

(21) word2vecTrain.py - [Requires Windows or Linux] A script for training a word2vec model on the parsed speeches from Hansard (from Step 20).

(22) word2vecRun.py - [Requires Windows or Linux] A script for running the w2v model trained on Hansard (from Step 21) and applying it to the Hansard transcripts of the video snippets (from Step 2).  

(23) w2vScores.csv - A csv file linking the transcripts of the video snippets (from Step 2) to the sentiment scores generated
using the word2vec model (from Step 22).  

(24) applySentimentR.R - A script for applying popular sentiment dictionaries in R to the extracted Video Transcripts (from Step 2). Dictionaries: Lexicoder, Sentiwordnet, Jockers-Rinker, HuLiu.  

(24.B) applySentimentR_ccED.R - A script for checking performance of Lexicoder with paragraph context.

(25) HansardExtractedVideoTranscripts_RSentiment.csv - A csv file of the sentiment scores produced in Step 24. 

(26) applySVMFastTextVader.py - A script that trains Support Vector Machines and FastText on a training subset of the IMDB movie review (https://www.kaggle.com/utathya/imdb-review-dataset) and Stanford handcoded tweet (https://snap.stanford.edu/data/twitter7.html) databases, and applies these models to a testing subset of each corpora. The script applies the models to classify the sentiment of the Hansard transcripts of the video snippets (from Step 2). The  script also scores the sentiment of these snippets using the Valence Aware Dictionary and Sentiment Reasoner (VADER - https://github.com/cjhutto/vaderSentiment) and LIWC (https://liwc.wpengine.com/) sentiment dictionaries. The training data and models are available at https://www.dropbox.com/sh/u91njzwcuvdu8oa/AABkl2vUJRUNEq4WEGSCBql_a?dl=0 (~1.5GB combined).

(27) hansardExtractedVideoTranscripts_SVMFastTextVader.csv - The csv file of the sentiment scores/classifications produced in Step 26.

(28) comparingEmbeddings.py - A script for comparing the performance of word2vec using different seed words and corpora. Produces seperate CSV for each comparison.

(29) Word2vec_iterative_corpus_reduction.ipynb - A Jupyter lab file for excracting random segments of the full corpus--reducing its size--and then training word embeddings on each derivative corpora.  

(30) w2vecSensitivity.R - An R file for comparing the results of the models generated from steps 28 and 29 above for predcting human judgments.

(31) emotionParliament.ipynb - A Jupyter lab file implementing the project workflow.  












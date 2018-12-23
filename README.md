# emotionParliament
The Automated Detection of Emotion in Transcripts of Parliamentary Speech: Comparing Human and Machine Classification of the Video and Written Records of Debates in the Canadian House of Commons

Abstract: The volume of machine-readable text communication about politics has increased exponentially over the past three decades, spawning the pursuit of new tools for automated analyses of sentiment in large political corpora.  Unlike written communication, however, the expression of emotion in speech is not confined to word-choice and syntax, and instead relies heavily on intonation, facial expressions, and body language, which go undetected in analyses of political text.  This raises the question of whether tools developed for analyses of writing can detect sentiment in transcripts of political speech.  In this paper, we survey a variety of strategies for the automated analysis of emotion in text, and test their outputs against human-coded sentiment analysis of the written and video record of debates in the Canadian House of Commons. We find that transcripts capture the valence, but not the emotional intensity, of political speeches. We also find that while leading dictionary and supervised approaches to sentiment detection performed reasonably well, using domain specific word embeddings induced from state-of-the-art Neural Networks surpassed these other approaches, and achieved near-human level performance. 

(1) selectionScript.R - A script for selecting video clips to extract from CPAC Question Periods.

(2) extractedSentencesYouTubeLinks.csv - The list of videos extracted from Step (1), along with date, speaker, party, language of speech, Hansard record (English), timeStamp (MM:SS), sentence length (SS:MS), and video link (youTube). 

(3) videoCodingInstrument.pdf - An image of the Qualtrics coding instrument for the video clips.

(4) emotionInHansard_December+20%2C+2018_14.52.csv - The raw output from the Qualtrics Survey Instrument used by the Video Coders.

(5) qualtricsDataExtract.py - A script for structuring the raw Qualtrics output (from 4).  

(6) qualtricsStructured.csv - The structured Qualtrics data (from 5).

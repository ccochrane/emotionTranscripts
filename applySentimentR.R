#T. Whyte and C. Cochrane

#####
# hansardSentiment.R
# Calculate a variety of sentiment scores for Hansard sentences
# Requires R-Studio
# Run from parent directory of "hansardExtractedVideoTranscripts.csv" 
#####

#--------------------------------------------------------------------------------------------
#initialization
#--------------------------------------------------------------------------------------------


library(dplyr)
library(tidytext)
library(sentimentr)
library(lexicon)
library(caret)
library(quanteda)
library(stringr)
library(rstudioapi) #Cochrane

#--------------------------------------------------------------------------------------------
#set directory to directory of script
#--------------------------------------------------------------------------------------------
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #Cochrane ed. Required RStudio

#--------------------------------------------------------------------------------------------
#randomization seed
#--------------------------------------------------------------------------------------------
set.seed(114647)

#--------------------------------------------------------------------------------------------
#import Data
#--------------------------------------------------------------------------------------------
data <- read.csv("hansardExtractedVideoTranscripts.csv", stringsAsFactors = FALSE)

#--------------------------------------------------------------------------------------------
#Apply Pre-Processing Scripts
#--------------------------------------------------------------------------------------------

# Import Lexicoder recommended text preprocessing functions downloaded from their site
source('LSDprep_jan2018.R') 

#define function for applying the processing 
preProcess <- function(string){
  lexiCoded <- LSDprep_contr(string) 
  lexiCoded <- LSDprep_dict_punct(lexiCoded)
  lexiCoded <- remove_punctuation_from_acronyms(lexiCoded)
  lexiCoded <- remove_punctuation_from_abbreviations(lexiCoded)
  lexiCoded <- LSDprep_punctspace(lexiCoded)
  lexiCoded <- LSDprep_negation(lexiCoded)
  return(lexiCoded)
}

newData = cbind(mutate(data, lexiProcessed=preProcess(english)))


#--------------------------------------------------------------------------------------------
# Functions for Applying LexiCoder
#--------------------------------------------------------------------------------------------

#newData <- lexiProcess(newData,"lexiProcessed")

#Application
lexicode <- function(){
  lex_corpus <- corpus(newData$lexiProcessed)
  dfm_lex <- dfm_weight(dfm(lex_corpus, dictionary=data_dictionary_LSD2015), scheme = "prop")
  f_lex <- textstat_frequency(dfm_lex, group = newData$Label)
  f_lex2 <- f_lex %>%
    mutate(group = as.integer(group)) %>%
    filter(feature == "positive" | feature ==  "negative") %>%
    mutate(frequency_score = if_else(feature=="negative", -1*frequency, frequency)) %>%
    group_by(group) %>%
    summarize(sentiment_lsd = sum(frequency_score)) 
  newData <- merge(newData, f_lex2, by.x="Label", by.y="group", all.x=TRUE)
  return(newData)
  
}

newData <- lexicode()


#--------------------------------------------------------------------------------------------
# Applying other Sentiment dictionaries
#--------------------------------------------------------------------------------------------


data_sentiment <- newData %>%
  mutate(sentences = get_sentences(as.character(english))) %>%
  mutate(sentiment_jockers_rinker = general_rescale(sentiment_by(sentences, by=NULL)$ave_sentiment)) %>%
  mutate(sentiment_sentiwordnet = general_rescale(sentiment_by(sentences, by=NULL, polarity_dt = hash_sentiment_sentiword)$ave_sentiment)) %>%
  mutate(sentiment_huliu = general_rescale(sentiment_by(sentences, by=NULL, polarity_dt = hash_sentiment_huliu)$ave_sentiment))                     
  sentences <- newData %>%
  group_by(Label) %>%
  mutate(linenumber = row_number())
         

  
### Export results to csv
write.table(data_sentiment, "hansardExtractedVideoTranscripts_RSentiment.tsv", sep="\t", row.names=FALSE, col.names=TRUE)  
  
  
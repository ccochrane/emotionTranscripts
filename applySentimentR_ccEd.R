library(sentimentr)

#####
# hansardSentiment.R
# Calculate a variety of sentiment scores for Hansard sentences
# Tanya Whyte and Chris Cochrane
#####

library(dplyr)
library(sentimentr)
library(lexicon)
library(caret)
library(quanteda)
library(stringr)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #Required RStudio


source('LSDprep_jan2018.R') # Import Lexicoder recommended text preprocessing functions downloaded from their site

set.seed(114647)

### Import Data
# Import the data file
# Note this is the original data file converted to UTF-8 .csv 
# and with an additional column of positive/negative codes I quickly performed on a subset of 500 speeches

data <- read.csv("hansardSentencesWithContext.csv")


### Lexicoder sentiment analysis

# Perform LSD text preprocessing functions from the code file provided on their site

data$lexiText <- LSDprep_contr(data$english) #replaces contractions
data$lexiText <- LSDprep_dict_punct(data$lexiText) #man. word sense disamb. using punctuation
data$lexiText <- LSDprep_punctspace(data$lexiText) #spaces around punctuation marks
data$lexiText <- LSDprep_negation(data$lexiText) #negations
data$lexiText <- LSDprep_dict(data$lexiText) #man. word sense disamb. using context
data$lexiText <- gsub('[[:punct:] ]+', ' ', data$lexiText) #remove punctuation, for wordcount
data$lexiText <- gsub('[[:digit:] ]+', ' ', data$lexiText) #remove numbers, for wordcount

data$lexiTextContext <- LSDprep_contr(data$EnglishContext)
data$lexiTextContext <- LSDprep_dict_punct(data$lexiTextContext)
data$lexiTextContext <- LSDprep_punctspace(data$lexiTextContext)
data$lexiTextContext <- LSDprep_negation(data$lexiTextContext)
data$lexiTextContext <- LSDprep_dict(data$lexiTextContext)
data$lexiTextContext <- gsub('[[:punct:] ]+', ' ', data$lexiTextContext) #remove punctuation, for wordcount
data$lexiTextContext <- gsub('[[:digit:] ]+', ' ', data$lexiTextContext) #remove numbers, for wordcount

lexicodeExpressive <- function(lexiText, label){
  txt <- lexiText
  label <- as.numeric(label) 
  toks <- tokens_compound(tokens(txt), data_dictionary_LSD2015)
  txtLen <- ntoken(toks)
  result <- dfm_lookup(dfm(toks), data_dictionary_LSD2015)
  nOfFeatures <- ntype(result)
  if (nOfFeatures > 0){
  neg <- result[1,1]
  pos <- result[1,2]
  negpos <- result[1,3]
  negneg <- result[1,4]
  #sent <- (pos+negneg-neg-negpos)/txtLen
  lexiWords <- as.numeric(pos+negneg+neg+negpos)
  sent <- (pos+negneg-neg-negpos)/lexiWords
  print(sprintf("----------- Label: %i", label))
  print(sprintf("Text: %s", txt))
  print(sprintf("Token Count: %i", txtLen))
  print(sprintf("Lexicoder Hits: %i", lexiWords))
  print(sprintf("Sentiment: %.4f", as.numeric(sent)))
  return(as.numeric(sent))
  } else {
    print(sprintf("----------- Label: %i", label))
    print(sprintf("Text: %s", txt))
    print(sprintf("Token Count: %i", txtLen))
    print(sprintf("Lexicoder Hits: %i", 0))
    print(sprintf("Sentiment: %s", NA))
    return(NA)
  }
}

data$LexiTextScore <- mapply(lexicodeExpressive, data$lexiText, data$Label)
data$LexiTextContextScore <- mapply(lexicodeExpressive, data$lexiTextContext, data$Label)

lexicodeExpressiveRawCount <- function(lexiText, label){
  txt <- lexiText
  label <- as.numeric(label) 
  toks <- tokens_compound(tokens(txt), data_dictionary_LSD2015)
  txtLen <- ntoken(toks)
  result <- dfm_lookup(dfm(toks), data_dictionary_LSD2015)
  nOfFeatures <- ntype(result)
  if (nOfFeatures > 0){
    neg <- result[1,1]
    pos <- result[1,2]
    negpos <- result[1,3]
    negneg <- result[1,4]
    #sent <- (pos+negneg-neg-negpos)/txtLen
    lexiWords <- as.numeric(pos+negneg+neg+negpos)
    sent <- (pos+negneg-neg-negpos)
    print(sprintf("----------- Label: %i", label))
    print(sprintf("Text: %s", txt))
    print(sprintf("Token Count: %i", txtLen))
    print(sprintf("Lexicoder Hits: %i", lexiWords))
    print(sprintf("Sentiment: %.4f", as.numeric(sent)))
    return(as.numeric(sent))
  } else {
    print(sprintf("----------- Label: %i", label))
    print(sprintf("Text: %s", txt))
    print(sprintf("Token Count: %i", txtLen))
    print(sprintf("Lexicoder Hits: %i", 0))
    print(sprintf("Sentiment: %s", NA))
    return(NA)
  }
}

data$LexiTextScoreRaw <- mapply(lexicodeExpressiveRawCount, data$lexiText, data$Label)
data$LexiTextContextScoreRaw <- mapply(lexicodeExpressiveCount, data$lexiTextContext, data$Label)




data_sentiment <- data %>%
  mutate(sentences = get_sentences(as.character(english))) %>%
  mutate(sentiment_jockers_rinker = general_rescale(sentiment_by(sentences, by=NULL)$ave_sentiment)) %>%
  mutate(sentiment_sentiwordnet = general_rescale(sentiment_by(sentences, by=NULL, polarity_dt = hash_sentiment_sentiword)$ave_sentiment)) %>%
  mutate(sentiment_huliu = general_rescale(sentiment_by(sentences, by=NULL, polarity_dt = hash_sentiment_huliu)$ave_sentiment))

data_sentiment <- subset(data_sentiment, select=-c(sentences))




write.csv(data_sentiment, "hansardVideoSentiment_lsdweightCCed.csv")







#C. Cochrane

#####
# predictTextCoderScores.R
# uses automatic sentiment scores to predict text coder scores
# Requires R-Studio
# Run from parent directory of "sentimentScores.csv" 
#####

#--------------------------------------------------------------------------------------------
#initialization
#--------------------------------------------------------------------------------------------


rm(list=ls())

library(boot)
library(ggplot2)
library(gtable)
library(Rmisc)
library(dplyr)
library(tidyverse)
library(caret)
source("http://peterhaschke.com/Code/multiplot.R")

setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) #Required RStudio
integratedScores <- read.csv("sentimentScores.csv")

w2vGoogleNews <- read.csv("w2vScoresGoogleNews.csv")
colnames(w2vGoogleNews)[colnames(w2vGoogleNews)=="sentiment"] <- "sent_w2vGoogleNews"
colnames(w2vGoogleNews)[colnames(w2vGoogleNews)=="IDMain"] <- "ID_main"

w2vGoodBadOnly <- read.csv("w2vGoodBadOnly.csv")
colnames(w2vGoodBadOnly)[colnames(w2vGoodBadOnly)=="sentiment"] <- "sent_w2vGoodBadOnly"
colnames(w2vGoodBadOnly)[colnames(w2vGoodBadOnly)=="IDMain"] <- "ID_main"

w2vExcellentTerribleOnly <- read.csv("w2vExcellentTerribleOnly.csv")
colnames(w2vExcellentTerribleOnly)[colnames(w2vExcellentTerribleOnly)=="sentiment"] <- "sent_w2vExcellentTerribleOnly"
colnames(w2vExcellentTerribleOnly)[colnames(w2vExcellentTerribleOnly)=="IDMain"] <- "ID_main"


w2vCorrectWrongOnly <- read.csv("w2vCorrectWrongOnly.csv")
colnames(w2vCorrectWrongOnly)[colnames(w2vCorrectWrongOnly)=="sentiment"] <- "sent_w2vCorrectWrongOnly"
colnames(w2vCorrectWrongOnly)[colnames(w2vCorrectWrongOnly)=="IDMain"] <- "ID_main"

w2vBestWorstOnly <- read.csv("w2vBestWorstOnly.csv")
colnames(w2vBestWorstOnly)[colnames(w2vBestWorstOnly)=="sentiment"] <- "sent_w2vBestWorstOnly"
colnames(w2vBestWorstOnly)[colnames(w2vBestWorstOnly)=="IDMain"] <- "ID_main"

w2vHereThereOnly <- read.csv("w2vHereThereOnly.csv")
colnames(w2vHereThereOnly)[colnames(w2vHereThereOnly)=="sentiment"] <- "sent_w2vHereThereOnly"
colnames(w2vHereThereOnly)[colnames(w2vHereThereOnly)=="IDMain"] <- "ID_main"

w2vFortunateUnfortunateOnly <- read.csv("w2vfortunateunfortunateOnly.csv")
colnames(w2vFortunateUnfortunateOnly)[colnames(w2vFortunateUnfortunateOnly)=="sentiment"] <- "sent_w2vFortunateUnfortunateOnly"
colnames(w2vFortunateUnfortunateOnly)[colnames(w2vFortunateUnfortunateOnly)=="IDMain"] <- "ID_main"

w2vPositiveNegativeOnly <- read.csv("w2vpositivenegativeOnly.csv")
colnames(w2vPositiveNegativeOnly)[colnames(w2vPositiveNegativeOnly)=="sentiment"] <- "sent_w2vPositiveNegativeOnly"
colnames(w2vPositiveNegativeOnly)[colnames(w2vPositiveNegativeOnly)=="IDMain"] <- "ID_main"

w2vHappyDisappointedOnly <- read.csv("w2vhappydisappointedOnly.csv")
colnames(w2vHappyDisappointedOnly)[colnames(w2vHappyDisappointedOnly)=="sentiment"] <- "sent_w2vHappyDisappointedOnly"
colnames(w2vHappyDisappointedOnly)[colnames(w2vHappyDisappointedOnly)=="IDMain"] <- "ID_main"

combined <- left_join(integratedScores, w2vGoogleNews, by="ID_main")
combined <- left_join(combined, w2vGoodBadOnly, by="ID_main")
combined <- left_join(combined, w2vExcellentTerribleOnly, by="ID_main")
combined <- left_join(combined, w2vCorrectWrongOnly, by="ID_main")
combined <- left_join(combined, w2vBestWorstOnly, by="ID_main")
combined <- left_join(combined, w2vHereThereOnly, by="ID_main")
combined <- left_join(combined, w2vFortunateUnfortunateOnly, by="ID_main")
combined <- left_join(combined, w2vPositiveNegativeOnly, by="ID_main")
combined <- left_join(combined, w2vHappyDisappointedOnly, by="ID_main")
#--------------------------------------------------------------------
# word2vec
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2v,data[indices,]))$r.squared,R=1000)

textw2vsent_sent <- model$t0
textw2vsent_sentLB <- quantile(model$t,.05)
textw2vsent_sentUB <- quantile(model$t,.95)
textw2vsent_sentLabel <- "w2v: \n Full Model \n Hansard"
textw2vsent_sentType <- "Machine"

predictingText <- data.frame(textw2vsent_sentLabel,
                             textw2vsent_sentType,
                             textw2vsent_sent, 
                             textw2vsent_sentLB, 
                             textw2vsent_sentUB)
names(predictingText) <- c("Label", "Type", "r2", "LB", "UB")

#--------------------------------------------------------------------
# word2vecGoogle
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vGoogleNews,data[indices,]))$r.squared,R=1000)

textw2vGooglesent_sent <- model$t0
textw2vGooglesent_sentLB <- quantile(model$t,.05)
textw2vGooglesent_sentUB <- quantile(model$t,.95)
textw2vGooglesent_sentLabel <- "w2v:\n Full Model \n Google News"
textw2vGooglesent_sentType <- "Machine"

dfTemp <- data.frame(textw2vGooglesent_sentLabel,
                             textw2vGooglesent_sentType,
                             textw2vGooglesent_sent, 
                             textw2vGooglesent_sentLB, 
                             textw2vGooglesent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# word2vecGoodBadOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vGoodBadOnly,data[indices,]))$r.squared,R=1000)

textw2vGoodBadOnlysent_sent <- model$t0
textw2vGoodBadOnlysent_sentLB <- quantile(model$t,.05)
textw2vGoodBadOnlysent_sentUB <- quantile(model$t,.95)
textw2vGoodBadOnlysent_sentLabel <- "w2v:\n\'Good\'\n\'Bad\'"
textw2vGoodBadOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vGoodBadOnlysent_sentLabel,
                     textw2vGoodBadOnlysent_sentType,
                     textw2vGoodBadOnlysent_sent, 
                     textw2vGoodBadOnlysent_sentLB, 
                     textw2vGoodBadOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# word2vecExcellentTerribleOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vExcellentTerribleOnly,data[indices,]))$r.squared,R=1000)

textw2vExcellentTerribleOnlysent_sent <- model$t0
textw2vExcellentTerribleOnlysent_sentLB <- quantile(model$t,.05)
textw2vExcellentTerribleOnlysent_sentUB <- quantile(model$t,.95)
textw2vExcellentTerribleOnlysent_sentLabel <- "w2v:\n\'Excellent\'\n\'Terrible\'"
textw2vExcellentTerribleOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vExcellentTerribleOnlysent_sentLabel,
                     textw2vExcellentTerribleOnlysent_sentType,
                     textw2vExcellentTerribleOnlysent_sent, 
                     textw2vExcellentTerribleOnlysent_sentLB, 
                     textw2vExcellentTerribleOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# word2vecCorrectWrongOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vCorrectWrongOnly,data[indices,]))$r.squared,R=1000)

textw2vCorrectWrongOnlysent_sent <- model$t0
textw2vCorrectWrongOnlysent_sentLB <- quantile(model$t,.05)
textw2vCorrectWrongOnlysent_sentUB <- quantile(model$t,.95)
textw2vCorrectWrongOnlysent_sentLabel <- "w2v:\n\'Correct\'\n\'Wrong\'"
textw2vCorrectWrongOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vCorrectWrongOnlysent_sentLabel,
                     textw2vCorrectWrongOnlysent_sentType,
                     textw2vCorrectWrongOnlysent_sent, 
                     textw2vCorrectWrongOnlysent_sentLB, 
                     textw2vCorrectWrongOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# word2vecBestWorstOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vBestWorstOnly,data[indices,]))$r.squared,R=1000)

textw2vBestWorstOnlysent_sent <- model$t0
textw2vBestWorstOnlysent_sentLB <- quantile(model$t,.05)
textw2vBestWorstOnlysent_sentUB <- quantile(model$t,.95)
textw2vBestWorstOnlysent_sentLabel <- "w2v:\n\'Best\'\n\'Worst\'"
textw2vBestWorstOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vBestWorstOnlysent_sentLabel,
                     textw2vBestWorstOnlysent_sentType,
                     textw2vBestWorstOnlysent_sent, 
                     textw2vBestWorstOnlysent_sentLB, 
                     textw2vBestWorstOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)

#--------------------------------------------------------------------
# word2vecHereThereOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vHereThereOnly,data[indices,]))$r.squared,R=1000)

textw2vHereThereOnlysent_sent <- model$t0
textw2vHereThereOnlysent_sentLB <- quantile(model$t,.05)
textw2vHereThereOnlysent_sentUB <- quantile(model$t,.95)
textw2vHereThereOnlysent_sentLabel <- "w2v:\n\'Here\'\n\'There\'"
textw2vHereThereOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vHereThereOnlysent_sentLabel,
                     textw2vHereThereOnlysent_sentType,
                     textw2vHereThereOnlysent_sent, 
                     textw2vHereThereOnlysent_sentLB, 
                     textw2vHereThereOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)

#--------------------------------------------------------------------
# word2vecFortunateUnfortunateOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vFortunateUnfortunateOnly,data[indices,]))$r.squared,R=1000)

textw2vFortunateUnfortunateOnlysent_sent <- model$t0
textw2vFortunateUnfortunateOnlysent_sentLB <- quantile(model$t,.05)
textw2vFortunateUnfortunateOnlysent_sentUB <- quantile(model$t,.95)
textw2vFortunateUnfortunateOnlysent_sentLabel <- "w2v:\n\'Fortunate\'\n\'Unfortunate\'"
textw2vFortunateUnfortunateOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vFortunateUnfortunateOnlysent_sentLabel,
                     textw2vFortunateUnfortunateOnlysent_sentType,
                     textw2vFortunateUnfortunateOnlysent_sent, 
                     textw2vFortunateUnfortunateOnlysent_sentLB, 
                     textw2vFortunateUnfortunateOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# word2vecPositiveNegativeOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vPositiveNegativeOnly,data[indices,]))$r.squared,R=1000)

textw2vPositiveNegativeOnlysent_sent <- model$t0
textw2vPositiveNegativeOnlysent_sentLB <- quantile(model$t,.05)
textw2vPositiveNegativeOnlysent_sentUB <- quantile(model$t,.95)
textw2vPositiveNegativeOnlysent_sentLabel <- "w2v:\n \'Positive\'\n\'Negative\'"
textw2vPositiveNegativeOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vPositiveNegativeOnlysent_sentLabel,
                     textw2vPositiveNegativeOnlysent_sentType,
                     textw2vPositiveNegativeOnlysent_sent, 
                     textw2vPositiveNegativeOnlysent_sentLB, 
                     textw2vPositiveNegativeOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)

#--------------------------------------------------------------------
# word2vecHappyDisappointedOnly
#--------------------------------------------------------------------

model <- boot(combined, function(data,indices)
  summary(lm(sent_textCoders~sent_w2vHappyDisappointedOnly,data[indices,]))$r.squared,R=1000)

textw2vHappyDisappointedOnlysent_sent <- model$t0
textw2vHappyDisappointedOnlysent_sentLB <- quantile(model$t,.05)
textw2vHappyDisappointedOnlysent_sentUB <- quantile(model$t,.95)
textw2vHappyDisappointedOnlysent_sentLabel <- "w2v:\n\'Happy\'\n\'Disappointed\'"
textw2vHappyDisappointedOnlysent_sentType <- "Machine"

dfTemp <- data.frame(textw2vHappyDisappointedOnlysent_sentLabel,
                     textw2vHappyDisappointedOnlysent_sentType,
                     textw2vHappyDisappointedOnlysent_sent, 
                     textw2vHappyDisappointedOnlysent_sentLB, 
                     textw2vHappyDisappointedOnlysent_sentUB)
names(dfTemp) <- c("Label", "Type", "r2", "LB", "UB")

predictingText <- rbind(predictingText, dfTemp)


#--------------------------------------------------------------------
# Graph All
#--------------------------------------------------------------------


graph_all <-ggplot(predictingText, aes(x=reorder(Label, -r2)), fill="grey") +
  geom_bar(aes(y=r2), stat="identity") +
  geom_errorbar(aes(ymin=LB, ymax=UB), width=0) +
  scale_fill_manual(values=c("red", "blue")) +
  theme(legend.position="bottom") +
  theme(axis.text.x = element_text(size=15),
        axis.text.y = element_text(size=15),
        axis.title.x = element_text(size=15),
        axis.title.y = element_text(size=15),
        legend.text = element_text(size=15),
        legend.title = element_blank()) +
  theme(panel.background=element_rect(fill="white")) +
  labs(x="\n Tools", y="R-Squared\n") +
  scale_y_continuous(limits=c(0,.46), breaks=c(.2, .4, .6), labels=scales::percent)

graph_all

ggsave("w2vSensitivity.pdf", device="pdf", width=15, height=10)



#--------------------------------------------------------------------
# Decaying Model Size
#--------------------------------------------------------------------

decayingScores <- read.csv("w2vApplyModelDecaySize.csv")

graph2 <- ggplot(decayingScores, aes(x=corpus_percent, y=rsquare, color=color)) +
  scale_color_continuous(low="red", high="blue", breaks=c(.18, 0, -.18), guide=FALSE) +
  geom_point(shape=1, size=5) +
  theme(axis.text.x = element_text(size=15)) +
  theme(axis.text.y = element_text(size=15)) +
  theme(panel.background=element_blank()) +
  theme(panel.grid.minor=element_line(color="grey")) + 
  theme(legend.text=element_text(size=15),
        legend.title=element_text(size=15)) +
  theme(axis.title.x = element_text(size=20)) +
  theme(axis.title.y = element_text(size=20)) +
  ylab("R-squared\n (Predicting Human Judgments)\n") +
  xlab("\n Corpus Size in Millions of Tokens (%)") +
  scale_x_reverse(breaks=seq(0,1,.1), labels=c( "0 (0%)", "7.7 (10%)", "15.4 (20%)", "23.0 (30%)", "30.7 (40%)", "38.4 (50%)", "46.1 (60%)", "53.8 (70%)", "61.4 (80%)", "69.1 (90%)", "76.8 (100%)")) +
  theme(axis.text.x = element_text(angle=90)) +
  scale_y_continuous(labels=scales::percent, limits=c(0,.45), breaks=c(0, .1, .2, .3, .4)) +
  geom_hline(yintercept=.26, linetype="dashed") +
  annotate("text", x=.85, y=.25, size=6, label="Lexicoder's Performance")



graph2

ggsave("w2vDecaySize.pdf", device="pdf", width=12, height=8)



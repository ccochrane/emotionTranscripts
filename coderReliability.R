#------------------------------------------------------------------------------------------------------
# C. Cochrane, 2018-01-03
# Description: Analyzes and graphs coder reliability. 
# Notes: (1) Require R-Studio
#------------------------------------------------------------------------------------------------------

remove(list=ls())
currentPath <- dirname(rstudioapi::getSourceEditorContext()$path)
print(currentPath)
#------------------------------------------------------------------------------------------------------
# Initialization
#------------------------------------------------------------------------------------------------------

library(foreign)
library(dplyr)
library(tidyverse)
library(irr)
library(lubridate)
library(data.table)
library(ggrepel)
library(RCurl)
#------------------------------------------------------------------------------------------------------
# Loading Data
#------------------------------------------------------------------------------------------------------

gitHub <- getURL("https://raw.githubusercontent.com/ccochrane/emotionParliament/master/fullCodingData.csv")
FCD <- read.csv(text = gitHub) #fullcodingdata


#------------------------------------------------------------------------------------------------------
# Creating Functions
#------------------------------------------------------------------------------------------------------

coderConsistency <- function(data, sent1, sent2, act1, act2, label,
                             howcoded = c("VIDEO", "TEXT", "MIXED"),
                             referent = c("SELF", "OTHER")){
  sent1 <- deparse(substitute(sent1))
  sent2 <- deparse(substitute(sent2))
  act1 <- deparse(substitute(act1))
  act2 <- deparse(substitute(act2))
  howcoded <- howcoded
  referent<- referent
  label <- label
  sent <- data %>%
    select(sent1, sent2)
  act <- data %>%
    select(act1, act2)

  sentConsistency <- icc(sent, model="twoway", type='consistency', unit='single')
  actConsistency <- icc(act, model="twoway", type='consistency', unit='single')
  
  result <- data.frame(label,
                       howcoded,
                       referent,
                       sentConsistency[7], 
                       sentConsistency[14],
                       sentConsistency[15],
                       actConsistency[7], 
                       actConsistency[14],
                       actConsistency[15])
  names(result) <- c("Label", "Type", "Referent",
                    "Sentiment", "SentimentLB", "SentimentUB",
                    "Activation", "ActivationLB", "ActivationUB")
  return(result)
}




#------------------------------------------------------------------------------------------------------
# Applying Functions
#------------------------------------------------------------------------------------------------------


T1T1.data <- coderConsistency(FCD, t1Sent1, t1Sent2, t1Act1, t1Act2,
                         label="T1T1", howcoded="TEXT", referent="SELF")

T1T2.data <- coderConsistency(FCD, t1SentAvg, t2SentAvg, t1ActAvg, t2ActAvg,
                              label="T1T2", howcoded="TEXT", referent="OTHER")

T1T3.data <- coderConsistency(FCD, t1SentAvg, t3SentAvg, t1ActAvg, t3ActAvg,
                              label="T1T3", howcoded="TEXT", referent="OTHER")

T2T3.data <- coderConsistency(FCD, t2SentAvg, t3SentAvg, t2ActAvg, t3ActAvg,
                              label="T2T3", howcoded="TEXT", referent="OTHER")

T2T2.data <- coderConsistency(FCD, t2Sent1, t2Sent2, t2Act1, t2Act2,
                              label="T2T2", howcoded="TEXT", referent="SELF")

T3T3.data <- coderConsistency(FCD, t3Sent1, t3Sent2, t3Act1, t3Act2,
                              label="T3T3", howcoded="TEXT", referent="SELF")

V1V1.data <- coderConsistency(FCD, v1Sent1, v1Sent2, v1Act1, v1Act2,
                              label="V1V1", howcoded="VIDEO", referent="SELF")

V1V2.data <- coderConsistency(FCD, v1SentAvg, v2SentAvg, v1ActAvg, v2ActAvg,
                              label="V1V2", howcoded="VIDEO", referent="OTHER")

V1V3.data <- coderConsistency(FCD, v1SentAvg, v3SentAvg, v1ActAvg, v3ActAvg,
                              label="V1V3", howcoded="VIDEO", referent="OTHER")

V2V3.data <- coderConsistency(FCD, v2SentAvg, v3SentAvg, v2ActAvg, v3ActAvg,
                              label="V2V1", howcoded="VIDEO", referent="OTHER")

V2V2.data <- coderConsistency(FCD, v2Sent1, v2Sent2, v2Act1, v2Act2,
                              label="V2V2", howcoded="VIDEO", referent="SELF")

V3V3.data <- coderConsistency(FCD, v3Sent1, v3Sent2, v3Act1, v3Act2,
                              label="V3V3", howcoded="VIDEO", referent="SELF")

V1T1.data <- coderConsistency(FCD, t1SentAvg, v1SentAvg, t1ActAvg, v1ActAvg,
                              label="V1T1", howcoded="MIXED", referent="OTHER")

V2T1.data <- coderConsistency(FCD, t1SentAvg, v2SentAvg, t1ActAvg, v2ActAvg,
                              label="V2T1", howcoded="MIXED", referent="OTHER")

V3T1.data <- coderConsistency(FCD, t1SentAvg, v3SentAvg, t1ActAvg, v3ActAvg,
                              label="V3T1", howcoded="MIXED", referent="OTHER")

V1T2.data <- coderConsistency(FCD, t2SentAvg, v1SentAvg, t2ActAvg, v1ActAvg,
                              label="V1T2", howcoded="MIXED", referent="OTHER")

V2T2.data <- coderConsistency(FCD, t2SentAvg, v2SentAvg, t2ActAvg, v2ActAvg,
                              label="V2T2", howcoded="MIXED", referent="OTHER")

V3T2.data <- coderConsistency(FCD, t2SentAvg, v3SentAvg, t2ActAvg, v3ActAvg,
                              label="V3T2", howcoded="MIXED", referent="OTHER")

V1T3.data <- coderConsistency(FCD, t3SentAvg, v1SentAvg, t3ActAvg, v1ActAvg,
                              label="V1T3", howcoded="MIXED", referent="OTHER")

V2T3.data <- coderConsistency(FCD, t3SentAvg, v2SentAvg, t3ActAvg, v2ActAvg,
                              label="V2T3", howcoded="MIXED", referent="OTHER")

V3T3.data <- coderConsistency(FCD, t3SentAvg, v3SentAvg, t3ActAvg, v3ActAvg,
                              label="V3T3", howcoded="MIXED", referent="OTHER")

#------------------------------------------------------------------------------------------------------
# Combining Data
#------------------------------------------------------------------------------------------------------

iccData <- rbind(V1V1.data, V1V2.data, V1V3.data, V1T1.data, V1T2.data, V1T3.data,
                 V2V2.data, V2V3.data, V2T1.data, V2T2.data, V2T3.data,
                 V3V3.data, V3T1.data, V3T2.data, V3T3.data,
                 T1T1.data, T1T2.data, T1T3.data,
                 T2T2.data, T2T3.data,
                 T3T3.data)
  

#------------------------------------------------------------------------------------------------------
# Graph Result
#------------------------------------------------------------------------------------------------------

iccData_graph <- ggplot(iccData, aes(x=Sentiment, y=Activation)) +
  geom_point(aes(color=Type, alpha=.5, shape=Referent), size=5) +
  scale_shape_manual(values=c(1, 16)) +
  geom_errorbarh(aes(xmin=SentimentLB, xmax=SentimentUB, color=Type, alpha=.7, linetype=Referent)) +
  geom_errorbar(aes(ymin=ActivationLB, ymax=ActivationUB, color=Type, alpha=.7, linetype=Referent)) +
  scale_linetype_manual(values=c("longdash", "solid")) +
  geom_text_repel(aes(label=Label, color=Type), size=8, show.legend=FALSE) +
  scale_x_continuous(limits=c(0,1))+
  scale_y_continuous(limits=c(0,1)) +
  geom_hline(yintercept=.5)+
  geom_vline(xintercept=.5)+
  xlab("\n Sentiment ICC") +
  ylab("Activation ICC \n") +
  scale_alpha(guide="none") +
  theme(panel.background=element_blank(),
        axis.text.x=element_text(size=20),
        axis.text.y=element_text(size=20),
        legend.text=element_text(size=20),
        legend.title=element_text(size=20),
        axis.title.x=element_text(size=20),
        axis.title.y=element_text(size=20),
        legend.position = "bottom")




iccData_graph

ggsave(filename=paste(currentPath, "coderReliability.pdf", sep="/"), width=10, height=10)




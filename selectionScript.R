#2018-01-20 C.Cochrane University of Toronto
"A script for generating a random set of timeStamps for
extracting sentences from House of Commons Debates"

library(lubridate)

## FILE PATHS
outpath <- "/Users/chriscochrane/Dropbox/Projects/Emotion in Hansard/clipSelections/" # (add your desination folder)
## META DATA
year <- 2017 #Enter Year (YYYY)
month <- 09 #Enter Month (1-12)
day <- 27 #Enter Day (1-31)
videoLength = "47:54" #Enter Length of Video (MM:SS)

##EXTRACTION POINTS
nOfExtractionPoints = 10 #Enter number of sentences to extract


## DEFINE RANDOMIZER
runRandomizer <- function(nOfExtractionPoints, videoLength) {
  #generates a set of n random numbers in the domain of 0 to k,
  #where n is the number of extraction points requested (line 9)
  #and k is the length of the video (line 7):
  timeStamps <- runif(nOfExtractionPoints, 0,as.period(ms(videoLength), unit="sec") )
  timeStamps <- round(seconds_to_period(timeStamps), digits=0) #rounding to nearest second
  timeStamps <- sort(timeStamps) #ascending order
  
  return(timeStamps)
}

##RUN RANDOMIZER
#Function accepts arguments for number of extraction points and
#lenth of the video. These are defined above.
extractionPoints <- runRandomizer(nOfExtractionPoints, videoLength)

## OUTPUT

subpath <- sprintf("%s-%s-%s%s", year, month, day,"/")
dir.create(file.path(outpath, subpath))

extractionPoints <- data.frame(extractionPoints) #creating dataframe
colnames(extractionPoints) <- c("timeStamp") #naming column
extractionPoints[c("Speaker", "French", "Party", "Length", 
                   "English Hansard", "Hansard Floor", 
                   "Google Translate")] <- NA #creating columns

write.csv(extractionPoints, file=sprintf("%s%s%s-%s-%s-%s%s", outpath, subpath,  year, month, day, "selections", ".csv"))
write.csv(extractionPoints, file=sprintf("%s%s%s-%s-%s-%s%s", outpath, subpath,  year, month, day, "final", ".csv"))


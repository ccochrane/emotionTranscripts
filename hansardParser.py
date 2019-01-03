#XML parser for Canadian Record of Parliamentary Debates
#version: C.Cochrane, 2018-01-03

######################################################################################################################
# OVERVIEW
######################################################################################################################
#Notes:     (1) Python 3.6 Anaconda
#           (2) Encoding UTF-8
#           (3) Runs from parent directory of Hansard folder.

#
#Modules:   (1) xml.etree.ElementTree
#               see https://docs.python.org/3.3/library/xml.etree.elementtree.html
#           (2) os
#               see https://docs.python.org/2/library/os.html
#           (3) re
#               see
#           (4) Pandas
#               see
#
# Data:     (1) xml from www.ourcommons.ca
#               (e.g., http://www.ourcommons.ca/DocumentViewer/en/42-1/house/sitting-200/hansard)
######################################################################################################################
# INITIALIZE
######################################################################################################################
#Load Modules
import xml.etree.ElementTree as ET
import re
import glob
import pandas as pd
from datetime import datetime
import pickle
import spacy

#Load Authority File

authorityFile = pickle.load( open("authorityFile.p", "rb"))



##########################################################################################################
# DEFINING FUNCTIONS FOR NLP TOOLS
##########################################################################################################
#Stopwords
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

#Spacy Parser
nlp = spacy.load('en')



######################################################################################################################
# Hansard XML Function for extracting Speeches and Metadata about Speeches
######################################################################################################################

def hansardXmlParserSpeeches(directory="Hansard/"): #accepts path of folder containing xml files



    # Notes re Structure of XML Schema from ourcommons.ca.
    #            (1) "Children" are categories that begin within some
    #                 other category. (denoted by a "tag")
    #            (2) "Parent" is the category within which some other
    #                 category begins.
    #            (3) "Geneology" traces parent-child connections back
    #                 through earlier generations. Geneological terms
    #                 are used here as they are in everyday speech (.e.g,
    #                 grandparents, great-grandparents, uncles, siblings...)
    #            (4)  "Attributes" are traits passed on to later
    #                 generations (children, etc). They are always shared by siblings.

    # Rules:
    #           (1) The Parliament's xml schema is not obviously hierarchical/linear.
    #               The following rules are necessary to make sense
    #               of the schema:
    #                   a) All parents pass down their attributes to their
    #                      children (forward inheritance).
    #                   b) All parents possess the attributes
    #                      of their children, even when the attribute first
    #                      appears at the level of the child (backward
    #                      inheritance for one level).
    #                   c) All siblings possess the same
    #                      attributes, even when the attribute is only listed for
    #                      one sibling and not the other (horizontal
    #                      inheritance).
    #                   d) Taking a), b) and c) together, attributes that first
    #                      appear in cousins are passed up to the cousin's
    #                      parent (i.e., aunt) via backward inheritance,
    #                      across to the the child's parent via horizontal
    #                      inheritance, and down to the child via forward
    #                      inheritance.  In short, children inherit the
    #                      attributes of their cousins.
    #
    # ================================================================

    dfList = []

    fileList = glob.glob(str(directory)+'*.XML')  #extract list of xml files from the indicated directory
    print("FileList", fileList)
    print("LengthOfFileList", len(fileList))
    for file in fileList:
        print(str(file))
    #Declaring variables and default values

    topLine=None
    secondLine=None
    orderOfBusinessRubric=None
    subjectOfBusinessTitle=None
    subjectOfBusinessID=None
    subjectOfBusinessQualifier = None
    speechId = None
    interventionId = None
    date = None
    year = None
    month = None
    day = None
    weekday = None
    speakerName = None
    affiliationType = None
    affiliationDbId = None
    floorLanguage = None
    speech = None
    mentionedEntityName = None
    mentionedEntityType = None


    for file in fileList:

        print("Currently Processing:", file)


        ##################
        ##################
        ##################
        #Part 1
        ##################
        ##################
        ##################

        file = str(file)


        with open(file, 'r', encoding='utf-8', errors='ignore') as xml_file:
            tree = ET.parse(xml_file)
        xml_file.close()



        root = tree.getroot()

        # Declaring to capture speakerIDs associated with each party

        capturedConId = []
        capturedLibId = []
        capturedNDPId = []
        capturedGrnId = []
        capturedFDId = []
        capturedIndId = []
        capturedBQId = []

        for elementHansard in root:
            #=================================================================
            # elementHansard is a part of the second generation (level).
            # ElementHansard has five children (tags): (1) StartPageNumber
            #                                          (2) DocumentTitle (ignored)
            #                                          (3) ExtractedInformation
            #                                          (4) HansardBody
            # Geneology: elementHansard is the child of root.
            # ================================================================

            if elementHansard.tag ==  "StartPageNumber":
                # =================================================================
                # StartPageNumber is a part of the third generation (level), has
                # one new attribute, and no children of its own.
                # genes:        (1) sourceStartPageNumber
                #
                # Geneology: StartPageNumber is the child of elementHansard, and
                # the grandchild of root.
                # ================================================================
                sourceStartPageNumber = int(elementHansard.text) #The page number of the first page for
                                                                 #this day in the Official Record of Debates.
            if elementHansard.tag == "ExtractedInformation":

                for elementExtractedInformation in elementHansard:
                    #==========================================================
                    # elementExtractedInformation is also part of the third
                    # generation (level). It is a sibling of StartPageNumber
                    # and therefore carries the attribute sourceStartPageNumber.
                    # "ExtractedInformation" has no children and 28 new
                    # attributes.
                    #               (1)  {'Name': 'InstitutionDebate'}
                    #               (2)  {'Name': 'Volume'}
                    #               (3)  {'Name': 'Number'}
                    #               (4)  {'Name': 'Session'}
                    #               (5)  {'Name': 'Parliament'}
                    #               (6)  {'Name': 'Date'}
                    #               (7)  {'Name': 'SpeakerName'}
                    #               (8)  {'Name': 'Institution'}
                    #               (9)  {'Name': 'Country'}
                    #               (10)  {'Name': 'TOCNote'} (ignored)
                    #               (11) {'Name': 'HeaderTitle'}
                    #               (12) {'Name': 'HeaderDate'}
                    #               (13) {'Name': 'MetaDocumentCategory'} (ignored)
                    #               (14) {'Name': 'MetaTitle'}
                    #               (15) {'Name': 'MetaTitleEn'}
                    #               (16) {'Name': 'MetaTitleFr'}
                    #               (17) {'Name': 'MetaVolumeNumber'}
                    #               (18) {'Name': 'MetaNumberNumber'}
                    #               (19) {'Name': 'MetaDateNumDay'}
                    #               (20) {'Name': 'MetaDateNumMonth'}
                    #               (21) {'Name': 'MetaDateNumYear'}
                    #               (22) {'Name': 'MetaCreationTime'}
                    #               (23) {'Name': 'MetaInstitution'}
                    #               (24) {'Name': 'InstitutionDebateFr'}
                    #               (25) {'Name': 'InstitutionDebateEn'}
                    #               (26) {'Name': 'ParliamentNumber'}
                    #               (27) {'Name': 'SessionNumber'}
                    #               (28) {'Name': 'InCameraNote'}
                    # Geneology: ExtractedInformation is the child of elementHansard,
                    #            the grandchild of root, and has no children of its
                    #            own. StartPageNumber, DocumentTitle, and
                    #            ExtractedInformation have properties shared by
                    #            all descendants of HansardBody, but they have
                    #            no children of their own.
                    #=========================================================

                    if elementExtractedInformation.attrib=={'Name': 'MetaInstitution'}: #e.g., House of Commons
                        chamber = elementExtractedInformation.text

                    if elementExtractedInformation.attrib=={'Name': 'ParliamentNumber'}: #Which Parliament Number
                        parliamentNumber = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'SessionNumber'}: #Which Session Number
                        parliamentSession = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'HeaderTitle'}: #E.g., "Commons Debates"
                        sourceTitle = elementExtractedInformation.text

                    if elementExtractedInformation.attrib=={'Name': 'MetaVolumeNumber'}: #Hansard Volume
                        sourceVolume = elementExtractedInformation.text

                    if elementExtractedInformation.attrib=={'Name': 'MetaNumberNumber'}: #Hansard Number
                        sourceNumber = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'HeaderDate'}: #Date in Format (January 1, 2001)
                        date = elementExtractedInformation.text

                    if elementExtractedInformation.attrib=={'Name': 'MetaDateNumYear'}: #Year
                        year = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'MetaDateNumMonth'}: #Month Number
                        month = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'MetaDateNumDay'}: #Day Number
                        day = int(elementExtractedInformation.text)

                    if elementExtractedInformation.attrib=={'Name': 'Date'}:
                        weekday = elementExtractedInformation.text.split(',',1)[0] #Day of Week, e.g., "Monday"

            if elementHansard.tag == "HansardBody":
                for elementHansardBody in elementHansard:
                # ======================================================================
                # elementHansard Body is also part of the third generation.  It is a
                # sibling of StartPageNumber and elementExtractedInformation, and thus
                # carries the attributes sourceStartPageNumber from startPageNumber, and the
                # 28 attributes from elementExtractedInformation.  elementHansardBody has 10
                # new genes (attributes) and two children (tags).
                # attrib:       (1)  {} #Empty
                #               (2)  {'id': '9796727', 'Rubric': 'Other'}
                #               (3)  {'id': '9794282', 'Rubric': 'StatementsByMembers'}
                #               (4)  {'id': '9794342', 'Rubric': 'NewMP'}
                #               (5)  {'id': '9794349', 'Rubric': 'OralQuestionPeriod'}
                #               (6)  {'id': '9794620', 'Rubric': 'RoutineProceedings'}
                #               (7)  {'id': '9794803', 'Rubric': 'Other'}
                #               (8)  {'id': '9796436', 'Rubric': 'Other'}
                #               (9)  {'id': '9796555', 'Rubric': 'RoutineProceedings'}
                #               (10)  {'id': '9796639', 'Rubric': 'LateShow'}
                # children:     (1)   Intro
                #               (2)   OrderOfBusiness
                # Geneology: elementHansardBody is the child of elementHansard, and the
                #            grandchild of root.  It has two children.  It shares all of
                #            the genes of its siblings, elementExtractedInformation and
                #            StartPageNumber, and it passes down all of these attribs to
                #            its two children.  It also has 10 new attribs of its own, for a
                #            total of 39 attribs that it passes down.
                # ======================================================================
                    if elementHansardBody.tag=="Intro":
                        for elementIntro in elementHansardBody:
                            #====================================================================
                            # elementIntro is a part of the fourth generation.  It has two new
                            # attribs and no children (tags).
                            # attribs:       (1) Paratext
                            #                (2) Prayer
                            # Geneology: elementIntro is the child of elementHansardBody, the
                            # grandchild of elementHansard, and the great-grandchild of root.
                            # elementIntro has two new genes and two children.  Although
                            # elementIntro's line dies off in this generation, its two genes are
                            # recorded here because they are shared by its sibling,
                            # OrderOfBusiness, and passed down through that lineage.
                            #====================================================================

                            if elementIntro.tag=="ParaText": #Attribute of elementIntro.  Procedural text in this case.
                                topLine = elementIntro.text #top line for the day.

                            if elementIntro.tag=="Prayer": #Attribute of elementIntro
                                secondLine = elementIntro.text

                    if elementHansardBody.tag=="OrderOfBusiness":
                        for elementOrderOfBusiness in elementHansardBody:
                            # ======================================================================
                            # elementOrderOfBusiness is also a part of the fourth generation, and therefore
                            # shares the two attributes of its sibling, elementIntro.  elementOrderOfBusiness
                            # has two additional new attributes. It has one child.
                            # genes:        (1)   OrderOfBusinessTitle
                            #               (2)   Catchline
                            # children:     (1)   SubjectOfBusiness
                            #
                            # Note: OrderOfBusinessTitle repeats Catchline.  It is therefore ignored.
                            #
                            # Geneology: elementOrderOfBusiness is the child of elementHansardBody,
                            # the grandchild of elementHansard, and the great-grandchild of root. It is
                            # the sibling of elementIntro.
                            # ======================================================================
                                if elementOrderOfBusiness.tag== "SubjectOfBusiness":
                                    for elementSubjectOfBusiness in elementOrderOfBusiness:
                                        subjectOfBusinessID = elementOrderOfBusiness.attrib.get("id") #stores official ID
                                        #========================================================================
                                        # elementSubjectOfBusiness is the fifth generation, and the only child
                                        # of elementOrderOfBusiness.  elementSubjectOfBusiness has 4 genes and
                                        # 1 child.
                                        # genes:        (1) Timestamp
                                        #               (2) FloorLanguage
                                        #               (3) SubjectOfBusinessTitle
                                        #               (4) SubjectOfBusinessQualifier
                                        #
                                        # children:     (1) SubjectOfBusinessContent
                                        #
                                        # Geneology: elementSubjectOfBusiness is the only child of
                                        # elementOrderofBusiness, the grandchild of elementHansardBody,
                                        # the great-grandchild of elementHansard, and the great-great-
                                        # grandchild of root.
                                        #========================================================================
                                        if elementSubjectOfBusiness.tag=="Timestamp":
                                            timeStampHr = elementSubjectOfBusiness.attrib['Hr']
                                            timeStampMin = elementSubjectOfBusiness.attrib['Mn']


                                        orderOfBusinessRubric = elementHansardBody.attrib['Rubric']  # A secondary description,
                                        #                                                              an attribute inherited from
                                        #                                                              elementHansardBody.
                                        #                                                              Needs to go with
                                        #                                                              each speech.
                                        if elementSubjectOfBusiness.tag=="FloorLanguage":
                                            floorLanguage = elementSubjectOfBusiness.attrib['language']

                                        if elementSubjectOfBusiness.tag=='SubjectOfBusinessTitle':     #A general title, procedurally oriented

                                            subjectOfBusinessTitle = elementSubjectOfBusiness.text
                                            subjectOfBusinessQualifier = "" #Not always available. resets so it doesn't get the previous qualifier

                                            if subjectOfBusinessTitle == "":
                                                subjectOfBusinessTitle = "NA"
                                                subjectOfBusinessQualifier = ""  # Not always available. resets so it doesn't get the previous qualifier


                                        if elementSubjectOfBusiness.tag=="SubjectOfBusinessQualifier":   #A more specific (and substantive title). Not always available.
                                            subjectOfBusinessQualifier = elementSubjectOfBusiness.text


                                        for elementSubjectOfBusinessContent in elementSubjectOfBusiness:
                                            # ========================================================================
                                            # elementSubjectOfBusinessContent is the sixth generation, and the only child
                                            # of elementSubjectOfBusiness.  elementSubjectOfBusinessContent has 2 attribs and
                                            # 1 child.
                                            # attribs:      (1) Timestamp
                                            #               (2) FloorLanguage
                                            #
                                            # children:     (1) Intervention
                                            #
                                            #
                                            # Geneology: elementSubjectOfBusinessContent is the only child of
                                            # elementSubjectofBusiness, the grandchild of elementOrderOfBusiness,
                                            # the great-great child of elementHansardBody, the great-great-grandchild of
                                            # elementHansard and the great-great-great grandchild of root.
                                            if elementSubjectOfBusinessContent.tag == "Timestamp": #Time Stamped every five mintues, at different levels.
                                                timeStampHr = elementSubjectOfBusinessContent.attrib['Hr']
                                                timeStampMin = elementSubjectOfBusinessContent.attrib['Mn']

                                            if elementSubjectOfBusinessContent.tag == "FloorLanguage":
                                                floorLanguage = elementSubjectOfBusinessContent.attrib['language']

                                            if elementSubjectOfBusinessContent.tag == "ParaText":  #This would be procedural text (e.g., It being 5:30 p.m., the House will now proceed to the taking of the....)
                                                pass

                                            if elementSubjectOfBusinessContent.tag == "Intervention": #This is an intervention

                                                for elementSubjectOfBusinessContentIntervention in elementSubjectOfBusinessContent:
                                                    # ========================================================================
                                                    # elementSubjectOfBusinessContentIntervention is the seventh generation,
                                                    # and the only child of elementSubjectOfBusinessContent.
                                                    # elementSubjectOfBusinessContentIntervention has two children:
                                                    #
                                                    # children:     (1) Person Speaking
                                                    #               (2) Content

                                                    #print(elementSubjectOfBusinessContent.attrib)
                                                    interventionId = elementSubjectOfBusinessContent.attrib.get("id")

                                                    if elementSubjectOfBusinessContentIntervention.tag=="PersonSpeaking":

                                                        for elementSubjectOfBusinessContentInterventionPersonSpeaking in elementSubjectOfBusinessContentIntervention:
                                                            # ========================================================================
                                                            # elementSubjectOfBusinessContentInterventionPersonSpeaking is the eigth generation,
                                                            # and child of elementSubjectOfBusinessContentIntervention.
                                                            # elementSubjectOfBusinessContentInterventionPersonSpeaking has one attributes:
                                                            #               (1) Affiliation
                                                            #                   (A) Affiliation Type
                                                            #                   (B) Affiliation DataBase ID
                                                            #                   (C) Affiliation Name (i.e. Speaker's Name)
                                                            if elementSubjectOfBusinessContentInterventionPersonSpeaking.tag=="Affiliation":

                                                                try:
                                                                    affiliationType = elementSubjectOfBusinessContentInterventionPersonSpeaking.attrib['Type']
                                                                except:
                                                                    affiliationType = "NA"

                                                                affiliationDbId = elementSubjectOfBusinessContentInterventionPersonSpeaking.attrib['DbId']

                                                                if elementSubjectOfBusinessContentInterventionPersonSpeaking.text is not None: #a couple of speaker names are missing
                                                                    speakerName = elementSubjectOfBusinessContentInterventionPersonSpeaking.text
                                                                else:
                                                                    speakerName = "NA"

                                                                capturedConId.append(214648) #Ambrose has multiple Aliases.  She seems to start with an old one.
                                                                capturedConId.append(214568)

                                                                capturedLibId.append(213924) #Lamoureux given different IDs for first and subsequent speeches

                                                                if "Justin Trudeau" in speakerName :
                                                                    party = 'Lib'
                                                                    capturedLibId.append(affiliationDbId)

                                                                if "Rona Ambrose" in speakerName:
                                                                    party = 'Con'
                                                                    capturedLibId.append(affiliationDbId)

                                                                elif "Thomas Mulcair" in speakerName:
                                                                    party == 'NDP'
                                                                    capturedNDPId.append(affiliationDbId)

                                                                elif "Stephen Harper" in speakerName:
                                                                    party = 'Con'
                                                                    capturedConId.append(affiliationDbId)

                                                                elif "Andrew Scheer" in speakerName:
                                                                    party = 'Con'
                                                                    capturedConId.append(affiliationDbId)

                                                                #Party
                                                                elif speakerName[-3:] == 'PC)':
                                                                    party = "Con"
                                                                    capturedConId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'b.)':
                                                                    party = 'Lib'
                                                                    capturedLibId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'DP)':
                                                                    party = 'NDP'
                                                                    capturedNDPId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'FD)':
                                                                    party = 'FD'
                                                                    capturedFDId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'GP)':
                                                                    party = 'Grn'
                                                                    capturedGrnId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'BQ)':
                                                                    party = 'BQ'
                                                                    capturedBQId.append(affiliationDbId)

                                                                elif speakerName[-3:] == 'd.)':
                                                                    party = 'Ind'
                                                                    capturedIndId.append(affiliationDbId)

                                                                elif affiliationDbId in capturedConId:
                                                                    party = 'Con'

                                                                elif affiliationDbId in capturedLibId:
                                                                    party = 'Lib'

                                                                elif affiliationDbId in capturedNDPId:
                                                                    party = "NDP"

                                                                elif affiliationDbId in capturedBQId:
                                                                    party = 'BQ'

                                                                elif affiliationDbId in capturedFDId:
                                                                    party = 'FD'

                                                                elif affiliationDbId in capturedGrnId:
                                                                    party = "Grn"

                                                                else:
                                                                    party = None
                                     

                                                    if elementSubjectOfBusinessContentIntervention.tag=="Content":
                                                        speech = [] #an empty list, which will collect speech fragements below.
                                                        paraNumRange = [] #empty list, for paragraph number range

                                                        documentType = []  # empty list, for any documents (Type) mentioned by speaker. Type is unlabelled integer.  (To Look up)
                                                        documentID = []  # empty list, for any documents mentioned by speaker.  This is a database ID. (To Look up)
                                                        documentTitleList = []  # mpty list, for title of any document mentioned by Speaker.  This is readable text.

                                                        mentionedEntityType = []  # empty list, for any Members mentioned in the speech.  This is unlabelled integer.  (To Look up)
                                                        mentionedEntityDbId = []  # empty list, for any Members mentioned in the speech.  This is a database ID. (To look up)
                                                        mentionedEntityNameList = []  # empty list, for names of any members mentioned in the speech.

                                                        for elementSubjectOfBusinessContentInterventionContent in elementSubjectOfBusinessContentIntervention:
                                                            # ========================================================================
                                                            # elementSubjectOfBusinessContentInterventionContent is the eigth generation,
                                                            # and child of elementSubjectOfBusinessContentIntervention.
                                                            # elementSubjectOfBusinessContentIntervention has three attributes:
                                                            #               (1) FloorLanguage
                                                            #               (2) TimeStemp
                                                            #               (3) ParaText
                                                            #
                                                            if elementSubjectOfBusinessContentInterventionContent.tag == "FloorLanguage":
                                                                floorLanguage = elementSubjectOfBusinessContentInterventionContent.attrib['language']

                                                            if elementSubjectOfBusinessContentInterventionContent.tag == "Timestamp":
                                                                timeStampHr = elementSubjectOfBusinessContentInterventionContent.attrib['Hr']
                                                                timeStampMin = elementSubjectOfBusinessContentInterventionContent.attrib['Mn']

                                                            if elementSubjectOfBusinessContentInterventionContent.tag == "ParaText":
                                                                try:
                                                                    paraNumRange.append(int(elementSubjectOfBusinessContentInterventionContent.attrib["id"]))
                                                                except:
                                                                    pass
                                                                phrase = ET.tostring(elementSubjectOfBusinessContentInterventionContent, method="text")
                                                                phrase = phrase.decode("UTF-8")
                                                                phrase = phrase.replace('\n', '').replace('\t', '')

                                                                speech.append(phrase)
                                                                speech.append("\n\n")


                                                                for elementSubjectOfBusinessContentInterventionContentParaText in elementSubjectOfBusinessContentInterventionContent:
                                                                    #print(elementSubjectOfBusinessContentInterventionContentParaText.tag)
                                                                    # ========================================================================
                                                                    # elementSubjectOfBusinessContentInterventionContentParaText is the ninth generation,
                                                                    # and child of elementSubjectOfBusinessContentIntervention.
                                                                    # elementSubjectOfBusinessContentIntervention has three attributes:
                                                                    #               (1) Document (Any Bills Mentioned)
                                                                    #               (2) Affiliation (Any Members Mentioned)
                                                                    #               (B) ParaText
                                                                    #
                                                                    # print(elementSubjectOfBusinessContentInterventionContent.tag)
                                                                    if elementSubjectOfBusinessContentInterventionContentParaText.tag=="Document":
                                                                        try:
                                                                            documentType.append(elementSubjectOfBusinessContentInterventionContentParaText.attrib['Type'])
                                                                        except:
                                                                            documentType.append("NA")
                                                                        try:
                                                                            documentID.append(elementSubjectOfBusinessContentInterventionContentParaText.attrib['DbId'])
                                                                        except:
                                                                            documentID.append("NA")
                                                                        try:
                                                                            documentTitle = elementSubjectOfBusinessContentInterventionContentParaText.text
                                                                        except:
                                                                            documentTitle = "NA"
                                                                        documentTitleList.append(documentTitle)

                                                                    if elementSubjectOfBusinessContentInterventionContentParaText.tag=="Affiliation":
                                                                        try:
                                                                            mentionedEntityType.append(elementSubjectOfBusinessContentInterventionContentParaText.attrib['Type'])
                                                                        except:
                                                                            mentionedEntityType.append("NA")
                                                                        try:
                                                                            mentionedEntityDbId.append(elementSubjectOfBusinessContentInterventionContentParaText.attrib['DbId'])
                                                                        except:
                                                                            mentionedEntityDbId.append("NA")
                                                                        mentionedEntityName = elementSubjectOfBusinessContentInterventionContentParaText.text
                                                                        mentionedEntityNameList.append(mentionedEntityName)



                                                        #################################################################
                                                        #Cleanup
                                                        #################################################################

                                                        speech = ''.join(speech)
                                                        for openquote in ['&#8220;']:
                                                            if openquote in speech:
                                                                speech=speech.replace(openquote,"\"")
                                                        for endquote in ['&#8221;']:
                                                            if endquote in speech:
                                                                speech=speech.replace(endquote,"\"")

                                                        speech = re.sub(r' Minister(?! )', 'Minister ', speech)
                                                        speech = re.sub(r'PrimeMinister', 'Prime Minister', speech)
                                                        speech = re.sub(r'Minister of Finance(?! )', 'Minister of Finance ', speech)
                                                        speech = re.sub(r'finance minister(?! )', 'finance minister ',speech)
                                                        speech = re.sub(r'Minister of Environment and Climate Change(?! )', 'Minister of Environment and Climate Change ',speech)

                                                        speechId = str(year) + "-" + str(month) +"-" + str(day) +"-" + str(interventionId)

                                                        
                                                        

                                                        speech_filtered = ""

                                                        if speech != None:
                                                            
                                                            speech_nlp = nlp(speech) # convering speech into Spacy doc
                                                            
                                                            for token in speech_nlp:
                                                                pair = "_".join([token.text, token.tag_])
                                                                speech_filtered = " ".join([speech_filtered, pair])


                                                            '''
                                                            df = df.append({'parliamentNumber': int(parliamentNumber),
                                                                            'parliamentSession': int(parliamentSession),
                                                                            'orderOfBusinessRubric': orderOfBusinessRubric,
                                                                            'subjectOfBusinessTitle': subjectOfBusinessTitle,
                                                                            'subjectOfBusinessID': subjectOfBusinessID,
                                                                            'subjectOfBusinessQualifier': subjectOfBusinessQualifier,
                                                                            'speechId': speechId,
                                                                            'party': party,
                                                                            'interventionId': interventionId,
                                                                            'date': date,
                                                                            'year': int(year),
                                                                            'month': int(month),
                                                                            'day': int(day),
                                                                            'weekday': weekday,
                                                                            'timeStamp': timeStampHr+":"+timeStampMin,
                                                                            'speakerName': speakerName,
                                                                            'affiliationType': affiliationType,
                                                                            'affiliationDbId': affiliationDbId,
                                                                            'floorLanguage': floorLanguage,
                                                                            'speech': speech,
                                                                             'mentionedDocumentsTitle': documentTitleList,
                                                                            'mentionedDocumentsId': documentID,
                                                                            'mentionedDocumentsType': documentType,
                                                                            'mentionedEntityName': mentionedEntityNameList,
                                                                            'mentionedEntityId': mentionedEntityDbId,
                                                                            'mentionedEntityType': mentionedEntityType,
                                                                            }, ignore_index=True)
                                                            '''



                                                            dateYMD = datetime.strptime(str(year)+"-"+str(month)+"-"+str(day), '%Y-%m-%d')
                                                            
                                                            #Calling from dictionary
                                                            
                                                            id = int(affiliationDbId)
                                                            
                                                            try:
                                                                parlInfoId = authorityFile[id]['parlInfoId']
                                                                fullName = authorityFile[id]['fullName']
                                                                firstName = authorityFile[id]['firstName']
                                                                lastName = authorityFile[id]['lastName']
                                                                middleName = authorityFile[id]['middleName']
                                                                sex = authorityFile[id]['sex']
                                                                visibleMinority = authorityFile[id]['visibleMinority']
                                                                indigenous = authorityFile[id]['indigenous']
                                                                dateOfBirth = authorityFile[id]['dateOfBirth']
                                                                isEstimateDOB = authorityFile[id]['isEstimateDOB']
                                                                birthProvince = authorityFile[id]['birthProvince']
                                                                birthCountry = authorityFile[id]['birthCountry']
                                                                firstDay = authorityFile[id]['firstDay']
                                                                provOfRiding = authorityFile[id]['provOfRiding']
                                                                parlInfoPage = authorityFile[id]['parlInfoPage']
                                                                daysInOffice = (dateYMD-firstDay).days
                                                                
                                                            except: #if not dictionary entry for this dbID
                                                                parlInfoId = "NA"
                                                                parlInfoId = "NA"
                                                                fullName = "NA"
                                                                firstName = "NA"
                                                                lastName = "NA"
                                                                middleName = "NA"
                                                                sex = "NA"
                                                                visibleMinority = "NA"
                                                                indigenous = "NA"
                                                                dateOfBirth = "NA"
                                                                isEstimateDOB = "NA"
                                                                birthProvince = "NA"
                                                                birthCountry = "NA"
                                                                firstDay = "NA"
                                                                provOfRiding = "NA"
                                                                parlInfoPage = "NA"
                                                                daysInOffice = "NA"
                                                            
                                                                                                               
                                                            if dateOfBirth != "NA":
                                                                if (dateOfBirth.year == 9999):
                                                                    age = "NA"
                                                                else:
                                                                    age = (dateYMD-dateOfBirth).days/365.25
                                                            else:
                                                                age = "NA"
                                                            
                                                            dfList.append([int(parliamentNumber),
                                                                      int(parliamentSession),
                                                                       orderOfBusinessRubric,
                                                                       subjectOfBusinessTitle,
                                                                       subjectOfBusinessID,
                                                                       subjectOfBusinessQualifier,
                                                                       speechId,
                                                                       interventionId,
                                                                       date,
                                                                       dateYMD,
                                                                       int(year),
                                                                       int(month),
                                                                       int(day),
                                                                       weekday,
                                                                       timeStampHr+":"+timeStampMin,
                                                                       speakerName,
                                                                       party,
                                                                       parlInfoId,
                                                                       fullName,
                                                                       firstName,
                                                                       lastName,
                                                                       middleName,
                                                                       sex,
                                                                       age,
                                                                       daysInOffice,
                                                                       visibleMinority,
                                                                       indigenous,
                                                                       dateOfBirth,
                                                                       isEstimateDOB,
                                                                       birthProvince,
                                                                       birthCountry,
                                                                       firstDay,
                                                                       provOfRiding,
                                                                       parlInfoPage,
                                                                       affiliationType,
                                                                       affiliationDbId,
                                                                       floorLanguage,
                                                                       speech,
                                                                       speech_filtered,
                                                                       documentTitleList,
                                                                       documentID,
                                                                       documentType,
                                                                       mentionedEntityNameList,
                                                                       mentionedEntityDbId,
                                                                       mentionedEntityType,
                                                                       file])



    labels = ['parliamentNumber', 
              'parliamentSession', 
              'orderOfBusinessRubric',
              'subjectOfBusinessTitle',
              'subjectOfBusinessID', 
              'subjectOfBusinessQualifier', 
              'speechId', 
              'interventionId',
              'date', 
              'dateYMD', 
              'year', 
              'month', 
              'day', 
              'weekday', 
              'timeStamp',
              'speakerName', 
              'party', 
              'parlInfoId', 
              'fullName', 
              'firstName', 
              'lastName', 
              'middleName',
              'sex', 
              'age', 
              'daysInOffice', 
              'visibleMinority', 
              'indigenous', 
              'dateOfBirth', 
              'isEstimateDOB', 
              'birthProvince', 
              'birthCountry', 
              'firstDay', 
              'provOfRiding', 
              'parlInfoPage',
              'affiliationType', 
              'affiliationDbId', 
              'floorLanguage',
              'speech', 
              'speechFiltered',
              'mentionedDocumentsTitle', 
              'mentionedDocumentsId', 
              'mentionedDocumentsType',
              'mentionedEntityName', 
              'mentionedEntityId',
              'mentionedEntityType', 
              'filename'
              ]


    df = pd.DataFrame.from_records(dfList, columns=labels)

    df.to_csv("hansardExtractedSpeechesFull.csv", sep='\t', encoding='utf-8')



hansardXmlParserSpeeches()


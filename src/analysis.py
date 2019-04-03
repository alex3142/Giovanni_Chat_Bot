# -*- coding: utf-8 -*-

import en_core_web_sm
import os
import rdflib
from nltk import Tree
import spacy

class SpacyText:
    """
    This is an object which contains the spacy doc and (more importantly) the
    lemmas as a string allowing use of 'in' and '.find' for python strings :)
    """

    def __init__(self, spacyDoc):
        self.Doc = spacyDoc
        self.Lemmas = " ".join(ele.lemma_ for index, ele in enumerate(spacyDoc))
        self.rootList = self.__FindRoot(spacyDoc)
        
        tempText = " ".join(ele.lower_ for index, ele in enumerate(spacyDoc))
        self.text = " " + tempText
        
    def __FindRoot(self, spacyDoc):
        
        """sometimes there are two roots of the parse tree like in the example 
        below:
            
        testText =  I bought tomatoes and organges but i do not have apples and olives
                   buy_VBD                       
             _________|________                   
            |              tomato_NNS            
            |          ________|___________       
        -PRON-_PRP  and_CC            organge_NNS
        
                     have_VB                                  
           _____________|______________________                
          |      |      |      |           apple_NNS          
          |      |      |      |       ________|_________      
        but_CC i_PRP  do_VBP not_RB and_CC           olive_NNS    
        
        
        
        """
        #take into account when there are two trees:
        rootList = []
        
        for tok in spacyDoc:
            if tok.head == tok:
                rootList.append(tok)
                
        return rootList
        
    def FindLemma(self, thisLemma):
        """
        This function finds and returns the spacy token corresponding to the 
        string 'thisLemma', this is useful because 1) it tells us the word is
        in the sentence. 2) it returns the spacy token which has a '.children' 
        property meaning we can search the subtree for sentence understanding
        
        output:
            existBool - boolean as to whether the lemma is in the sentence
            tokenList - list of spacy token of the word of interest
            nTokens - int, the number times the lemms is found
        """
        # if we have two or more instances of this lemma we can put them
        # into a list and retuen all
        tokenList = []
        
        # this is needed because sometimes the verb "suggest" is triggered 
        # when the noun "suggestion" is found since in is a sub
        tempLemma = thisLemma + " "
        
        tempLemmaString = self.Lemmas
        
        # because we have added the requirement for a space at the end of the 
        # lemma we are checking for this will case probalems if the 
        # lemma is the last word of the sentence, 
        lastChar = tempLemmaString[-1]
        
        if lastChar.isalpha():
            # if it's a letter we add on a space 
            tempLemmaString = tempLemmaString + " "
        else:
            # if the last char is not a letter assume it's punctuation
            # so replace with a space
            tempLemmaString = tempLemmaString[:-1] + " "
            
        #print("tempLemma = ",tempLemma)
        #print("tempLemmaString = ",tempLemmaString)        
        if tempLemma in tempLemmaString:
            
            
            #if lemma is in string, find it and return it
            for index, ele in enumerate(self.Doc):
                if ele.lemma_ == thisLemma:
                    tokenList.append(ele)
                    existBool = True
          
        else:
            existBool = False

        return existBool, tokenList


class Analyzer:

    def __init__(self, ontology):
        self.nlp = en_core_web_sm.load()
        self.ontologyAnalysis = ontology

        self.ingredientObject = self.ontologyAnalysis.get_class_resource("food")
        self.cuisineObject = self.ontologyAnalysis.get_class_resource("cuisine")
        self.userObject = self.ontologyAnalysis.get_class_resource("person")
        self.recipeObject = self.ontologyAnalysis.get_class_resource("recipe")
        
        
    
    def __tok_format(self, tok):
        return "_".join([tok.lemma_, tok.tag_])


    def __to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(self.__tok_format(node), [self.__to_nltk_tree(child) for child in node.children])
        else:
            return self.__tok_format(node)
     
    def PrintTree(self, parsedText):
        """
        This function prints the shallow syntax tree to the console for 
        debugging, could also be used to show the processing during the demo...
        """

        [self.__to_nltk_tree(sent.root).pretty_print() for sent in parsedText.sents]
        
    def CheckChildren(self, node, valueOfInterestList, negativeList):
        """
        This function checks the children of nodes of interest to try and 
        understand what is being asked
        """
        # flag for if one of the values of interest is in the children
        valueInChildren = False
        
        # flag for negatives in the children 
        negativeInChildren = False
        
        # gives the lemmas found, used when
        # it is then required to investigate 
        # further the children
        lemmaFoundToken = None
        
        #print("CheckChildren = ", " ".join(ele.lemma_ for index, ele in enumerate(node.children)))
        
        # loop through children
        for index, ele in enumerate(node.children):
            # check for a verb of interest
            for item in valueOfInterestList:
                if item == ele.lemma_:
                    valueInChildren = True
                    lemmaFoundToken = ele
            # check for a negation 
            for item in negativeList:
                
                if item == ele.lemma_:
                    negativeInChildren = True
        
        
        return valueInChildren, negativeInChildren, lemmaFoundToken
    
    
    def __SearchOntologyRecursive_Placeholder(self, thisToken):
        
        # if the item is a spacy token we are a asking the ontology 
        if isinstance(thisToken,spacy.tokens.token.Token):
            return self.ontologyAnalysis.get_class_resource(thisToken.lemma_)
            
#            if listFromAnalysis.lemma_ == 'italian':
#                return True, 'italianCuisineObject'
#            elif listFromAnalysis.lemma_ == 'chinese':
#                return True, 'chineseCuisineObject'
#            elif listFromAnalysis.lemma_ == 'spanish':
#                return True ,'spanishCuisineObject'
#            elif listFromAnalysis.lemma_ == 'vegetarian':
#                return True ,'vegetarianCuisineObject'
#            elif listFromAnalysis.lemma_ == 'chicken':
#                return True, 'chickenFoodObject'
#            elif listFromAnalysis.lemma_ == 'rice':
#                return True, 'riceFoodObject'
#            elif listFromAnalysis.lemma_ == 'tomato':
#                return True, 'tomatoFoodObject'
#            else:
#                return False, False
    
    def __SearchOntology_Placeholder(self, listFromAnalysis):
        
        # if the item is a spacy token we are a asking the ontology 
        if isinstance(listFromAnalysis,spacy.tokens.token.Token):
            
            if listFromAnalysis.lemma_ == 'italian':
                return ['cuisineObject','italianCuisineObject']
            elif listFromAnalysis.lemma_ == 'chinese':
                return ['cuisineObject','chineseCuisineObject']
            elif listFromAnalysis.lemma_ == 'spanish':
                return ['cuisineObject','spanishCuisineObject']
            elif listFromAnalysis.lemma_ == 'vegetarian':
                return ['cuisineObject','vegetarianCuisineObject']
            elif listFromAnalysis.lemma_ == 'chicken':
                return ['ingredientObject','chickenFoodObject']
            elif listFromAnalysis.lemma_ == 'rice':
                return ['ingredientObject','riceFoodObject']
            elif listFromAnalysis.lemma_ == 'tomato':
                return ['ingredientObject','tomatoFoodObject']
            else:
                return None
            
        else:
        
            outputList = []
            
            for item in listFromAnalysis:
            
                if item == "user":
                    outputList.append("UserObject")
                elif item == "wants":
                    outputList.append("WantsRelationship")
                elif item == "NOTwants":
                    outputList.append("NotWantsRelationship")
                elif item == "has":
                    outputList.append("HasRelationship")
                elif item == "NOThas":
                    outputList.append("NotHasRelationship")
                elif item == "recipe":
                    outputList.append("RecipeObject")
                elif item == "agreement":
                    outputList.append("AgreementObject")
                elif item == "NOTagreement":
                    outputList.append("NotAgreementObject")
                elif item == "cuisine":
                    outputList.append("CuisineObject")
                else:
                    outputList.append(item)
                    
            if isinstance(listFromAnalysis,tuple):
                return tuple(outputList)
            else:
                return outputList
    
    def __SearchOntologyType_Placeholder(self, token):
        
        """
        This function is needed to understand the object type
        (either cuisine or ingredient) because we need to know
        the relationship type to send out of the analysis
        a user HAS ingredients but WANTS cuisine
        
        input:
        token - spacy token object
        
        output:
        list [high level type, specific object type ]
        
        """

        
        
        if token == 'italianCuisineObject':
            return ['cuisineObject','italianCuisineObject']
        elif token == 'chineseCuisineObject':
            return ['cuisineObject','chineseCuisineObject']
        elif token == 'spanishCuisineObject':
            return ['cuisineObject','spanishCuisineObject']
        elif token == 'vegetarianCuisineObject':
            return ['cuisineObject','vegetarianCuisineObject']
        elif token == 'chickenFoodObject':
            return ['ingredientObject','chickenFoodObject']
        elif token == 'riceFoodObject':
            return ['ingredientObject','riceFoodObject']
        elif token == 'tomatoFoodObject':
            return ['ingredientObject','tomatoFoodObject']
        else:
            return [None,None]
        
    
    
    def InvestigateSentence(self, parsedText):
        """
        This function takes a parsed text and investigates the syntax tree
        to understand what is being asked, it sends info into the 
        ontology and returns a list of tuple triplets
         e.g. ('user', 'wants', 'recipe')
        """
        
        # stores the output, possibly could have been named better...
        outputList = []
        
        # bool to decide whether to continue analisys
        # there are 3/4 different opening options we 
        # are assessing here,
        
        ###########################################################
        ################## Check for greeting #####################
        ###########################################################
        
        # maybe the perdon has just said hello and no other info
        # it would be rude not to reply...
        
        greetingWords = ['hi', 'hello', 'hey','morning','afternoon']
        
        for thisWord in greetingWords:
    
            #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisWord)
            
            if tempBool:
                outputList.append((self.userObject,'greeting'))
                
        ###########################################################
        ################## Check for farewell #####################
        ###########################################################
        
        # maybe the perdon has just said hello and no other info
        # it would be rude not to reply...
        
        greetingWords = ['bye', 'laters', 'goodbye']
        
        for thisWord in greetingWords:
    
            #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisWord)
            
            if tempBool:
                outputList.append((self.userObject,'farewell'))
                
        ###########################################################
        ################## Check for swearing #####################
        ###########################################################
        
        # maybe the perdon has just said hello and no other info
        # it would be rude not to reply...
        
        swearWords = ['fuck you', 'fuck off', 'dick head', 'go screw yourself']
        
        for thisWord in swearWords:
            if thisWord in parsedText.text:
                outputList.append((self.userObject,'swearing'))
        

                
        ###########################################################
        ################## Check for agreement #####################
        ###########################################################
        
        # maybe the perdon has just said hello and no other info
        # it would be rude not to reply...
        
        agreementWords = ['yeah', 'yes', ' sure','fine','right','correct','thanks',' ok']
        
        #print("parsedText.text = ", parsedText.text)
        
        for thisWord in agreementWords:
    
            if thisWord in parsedText.text:
                outputList.append((self.userObject,'agreement'))
            
                
        ###########################################################
        ############### Check for disagreement ####################
        ###########################################################
        
        # maybe the perdon has just said hello and no other info
        # it would be rude not to reply...
        
        notAgreementWords = ['no', 'nope', 'wrong','incorrect']
        
        for thisWord in notAgreementWords:
    
            #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisWord)
            
            if tempBool:
                outputList.append((self.userObject,'NOTagreement'))
                
        ###########################################################
        ################ check for indifference ###################
        ###########################################################
        indifferencePhrases = ['whatever', "i don't mind", "i don't care", 'any','either']
        
        for thisWord in indifferencePhrases:
            if thisWord in parsedText.text:
                outputList.append((self.userObject,'indifferent'))
        
        ###########################################################
        ############ assume start of the converation ##############
        ###########################################################
        mainRequestVerbList = ['recommend', 'suggest', 'propose']
        secondaryVerbList = ['need', 'give', 'want','like']
        mainNounList = ['meal', 'food', 'recipe','something']
        secondaryNounList = ['suggestion', 'idea', 'recommendation']
        negativeList = ['not']
        
        sentenceType_3_firstVerb = ['want','need']
        sentenceType_3_secondVerb = ['cook','eat', 'make']

        
        ##########################################################
        ################ some explanation of lists ###############
        ##########################################################
        """
        Sentence Type 1
        
        mainRequestVerbList is used to find sentences like this, where the main
        verb of the sentence is a 'suggest' type word directly connected to 
        a 'recipe' type word
        
               suggest_VB          
           ________|__________      
          |        |      recipe_NN
          |        |          |     
        can_MD -PRON-_PRP    a_DT
        
            suggest_VB                 
           ________|_______________        
          |        |       |  something_NN/a recipe
          |        |       |       |       
          can_MD -PRON-_PRP ?_.  italian_JJ 

        ____________________________________________________________________
        
        Sentence Type 2
        
        secondaryVerbList is used to find sentences where the main verb is a 
        request type verb which is attached to either a 'recipe' type word or a 
        'suggestion' type word which is then attached to a 'recipe' type word
        
               need_VBP                        
            ______|___________                  
           |            suggestion_NN          
           |       ___________|___________      
         i_PRP   a_DT                 recipe_JJ
         
         or this
         
               need_VBP          
            ______|_________      
           |            recipe_NN
           |                |     
         i_PRP             a_DT 

     
     ________________________________________________________________________
     
     sentence Type 3
     
     this sentence type has two verbs separating the recipe type word from the 
     root
     
               want_VBP                           
        __________|______________                  
       |    |     |           cook_VB             
       |    |     |        ______|_________        
       |    |     |       |           something_NN
       |    |     |       |                |       
     hi_UH ,_,  i_PRP   to_TO          italian_JJ 
     


    """
        
        ###############################################################
        #### check if this sentence is one of requesting a recipe #####
        ###############################################################
        
        # NOTE - this only works for the first lemma found
        # if there are multiple lemmas of interest in the sentence subsequent
        # lemmas will be ignored
        
        #assume no recipe is requested unless we see evidence
        recipeRequested = False
        
        ###### sentence type 1 ####
        
        # check to see if main verb is in sentence
        for thisVerb in mainRequestVerbList:
    
            #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisVerb)
            
            if tempBool:
                for item in tempTokenList:
                    valueInChildren_1, negativeInChildren_1 , _ = self.CheckChildren(item, mainNounList, negativeList)
                    #print ("valueInChildren_1 = ", valueInChildren_1)
                    #print ("negativeInChildren_1 = ", negativeInChildren_1)
                    
                    if valueInChildren_1 and (not negativeInChildren_1):
                        # we know the relationships here so we just need to 
                        # send this information into the ontology
                        # to get the specific objects
                        ontologyObjectOutput = (self.userObject,'wants', self.recipeObject)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)
                        
                        recipeRequested = True
                        
                    elif valueInChildren_1 and negativeInChildren_1:
                        
                        ontologyObjectOutput = (self.userObject,'NOTwants', self.recipeObject)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)
                        
                        recipeRequested = True
                    else:
                        ontologyObjectOutput = (self.userObject,'wants', None)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)
                
        ###### sentence type 2 ####
        
        # check if secondary verb is in the sentence
    
        for thisVerb in secondaryVerbList: #secondaryVerbList = ['need', 'give', 'want']
            
             #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisVerb)
        
            if tempBool:
            
                
                #first check of the secondary verb is directly connected to a
                # 'recipe' type word e.g. "i need a recipe"
                
                # check children 
                valueInChildren_2, negativeInChildren_2, _ = self.CheckChildren(tempTokenList[0], mainNounList, negativeList)
                #mainNounList = ['meal', 'food', 'recipe','something']
                
                if valueInChildren_2 and (not negativeInChildren_2):
                                        
                    ontologyObjectOutput = (self.userObject,'wants', self.recipeObject)
                    #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                    outputList.append(ontologyObjectOutput)
                    
                    recipeRequested = True
                    
                elif valueInChildren_2 and negativeInChildren_2:
                    
                    ontologyObjectOutput = (self.userObject,'NOTwants', self.recipeObject)
                    #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                    outputList.append(ontologyObjectOutput)
                    
                    recipeRequested = True
                else:
                    #now check for noun between verb and 'recipe' type word
                    # e.g. I need a recipe SUGGESTION
                    
                    # check children 
                    valueInChildren_3, negativeInChildren_3, wordTokenFound = self.CheckChildren(tempTokenList[0], secondaryNounList, negativeList)
                    # secondaryNounList = ['suggestion', 'idea', 'recommendation']
                
                    if valueInChildren_3:
                        #now loop through all the children to see if any of 
                        # them are recipe related words
                        
                        valueInChildren_4, negativeInChildren_4, wordTokenFound = self.CheckChildren(wordTokenFound, mainNounList, negativeList)
                    
                        #NOTE - we include the negativeInChildren_2 here because  the 
                        # negative may be attached to either
                        
                        if valueInChildren_4 and (not (negativeInChildren_4 or negativeInChildren_2)):
                            
                            ontologyObjectOutput = (self.userObject,'wants', self.recipeObject)
                            #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                            outputList.append(ontologyObjectOutput)
                        
                            recipeRequested = True
                        elif valueInChildren_4 and (negativeInChildren_4 or negativeInChildren_2):
                        
                            ontologyObjectOutput = (self.userObject,'NOTwants', self.recipeObject)
                            #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                            outputList.append(ontologyObjectOutput)
                        
                            recipeRequested = True
                        else:
                            ontologyObjectOutput = (self.userObject,'wants', None)
                            #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                            outputList.append(ontologyObjectOutput)
                            
                            
        ###### sentence type 3 ####
        
        # check if sentenceType_3_firstVerb is in the sentence
    
        for thisVerb in sentenceType_3_firstVerb: #secondaryVerbList = ['need', 'give', 'want']
            
             #find lemma in sentence
            tempBool, tempTokenList = parsedText.FindLemma(thisVerb)
        
            if tempBool:
            
                
                #first check of the secondary verb is directly connected to a
                # 'recipe' type word e.g. "i need a recipe"
                
                # check children 
                valueInChildren_2, negativeInChildren_2, wordTokenFound = self.CheckChildren(tempTokenList[0], sentenceType_3_secondVerb, negativeList)
                #sentenceType_3_secondVerb
                
                if valueInChildren_2:
                    

                        
                    valueInChildren_3, negativeInChildren_3, wordTokenFound = self.CheckChildren(wordTokenFound, mainNounList, negativeList)
                
                    #NOTE - we include the negativeInChildren_2 here because  the 
                    # negative may be attached to either
                    
                    if valueInChildren_3 and (not (negativeInChildren_3 or negativeInChildren_2)):
                        
                        ontologyObjectOutput = (self.userObject,'wants', self.recipeObject)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)
                    
                        recipeRequested = True
                    elif valueInChildren_3 and (negativeInChildren_3 or negativeInChildren_2):
                    
                        ontologyObjectOutput = (self.userObject,'NOTwants', self.recipeObject)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)
                    
                        recipeRequested = True
                    else:
                        ontologyObjectOutput = (self.userObject,'wants', None)
                        #ontologyObjectOutput = self.__SearchOntology_Placeholder(tempOutput)
                        outputList.append(ontologyObjectOutput)

                            
        ###############################################################
        ########### check if recipe cuisine is mentioned ##############
        ###############################################################
        # if a recipe has been requested see if one of the attached
        
        if recipeRequested:
            
            for thisNoun in mainNounList:# mainNounList = ['meal', 'food', 'recipe','something']
                
                #find lemma in sentence
                tempBool, tempTokenList = parsedText.FindLemma(thisNoun)
                
                #print("i want to cook an italian recipe with carrots")
                
                if tempBool:
                    # now we need to investigate the children to see if there is 
                    # positive and/or negative lists
                    #
                    # e.g.
                    # "i want to cook something italian or french but not english"
                    

                    positiveList, negativeList = self.__InvestigateChildNodesRecusive(tempTokenList[0])
                    
                    #positive and negtive list (i think) ae filled with 
                    # ontology objects so we can now just compare them 
                    # to parents to see what the relationship type is 
                    # (wants means cuising - user WANTS cuisine)
                    # (has means ingredients - user HAS ingredients)
                    
                    for item in positiveList:
                        #see if the item is known about in the ontology  
                        #if it is the tuple is (relationship type, ontology object)
                        # if not not it's (None, None)
                        
                        if self.ontologyAnalysis.is_subclass(item,self.cuisineObject):

                           ontologyObjectOutput = (self.userObject,'WantsRelationship',item)
                           outputList.append(ontologyObjectOutput)
                           
                        elif self.ontologyAnalysis.is_subclass(item,self.ingredientObject):
                            
                           ontologyObjectOutput = (self.userObject, 'HasRelationship',item)
                           outputList.append(ontologyObjectOutput)
                           
                           
                    for item in negativeList:
                        #see if the item is known about in the ontology
                        #if it is the tuple is (relationship type, ontology object)
                        # if not not it's (None, None)

                        if self.ontologyAnalysis.is_subclass(item,self.cuisineObject):
 
                           ontologyObjectOutput = (self.userObject,'NotWantsRelationship',item)
                           outputList.append(ontologyObjectOutput)
                           
                        elif self.ontologyAnalysis.is_subclass(item,self.ingredientObject):
                            
                           ontologyObjectOutput = (self.userObject, 'NotHasRelationship',item)
                           outputList.append(ontologyObjectOutput)
                             
    
        return outputList
    
    def __SearchOntology_Old(self, token):
     
        if token.lemma_ in ['tomato','olive','rice', 'onion']:
            return True, (token, 'Veg')
        elif token.lemma_ in ['chicken','pork']:
            return True, (token, 'meat')
        else:
            return False, None 
        
    # if token.lemma_ in ['italian','indian','french']:
    #     return 'cuisine'
    # elif token.lemma_ in ['tomato','rice','apple']:
        
     
    def __HasNegative(self, token):
        if token.lemma_ in ["not", "no"]:
            return True
        else:
            return False
    
    def __InvestigateChildNodesRecusive(self, token):
        countChildren = 0
        thisOutputPositive = []
        thisOutputNegative = []
        #need to assign the negative to the entire sub-tree 
        # not NOT assign it to nodes above on the tree
        negativeInChildren = False
        #print("token,lemma_ = ",token.lemma_ )
#        for tok in token.children:
#            print("child = ",tok.lemma_)
        
        for tok in token.children:
            countChildren += 1
            tempOutputListPositive, tempOutputListNegative = self.__InvestigateChildNodesRecusive(tok)
            # is there a negative in any one of the children
            # the output should be True
            if not negativeInChildren:
                negativeInChildren = self.__HasNegative(tok)
            
            if len(tempOutputListPositive) > 0:
                thisOutputPositive.append(tempOutputListPositive)
                
                # Flatten List (sorry Roberto!)
                #print(" - - - - - - - - - - - - - - - -")
               # print("thisOutputPositiveBEFORE = ",thisOutputPositive)
                
                #print("PROBLEM IS HERE, SOMETIMES DO NOT WANT THE SUBLIST....")
                
                newThisOutputPositiveList = []
                
                for mainListItem in thisOutputPositive:
                    if isinstance(mainListItem, list):
                        for innerListItem in mainListItem:
                            if isinstance(innerListItem, list):
                                for thisListShouldntExist in innerListItem:
                                    newThisOutputPositiveList.append(thisListShouldntExist)
                            else:
                                newThisOutputPositiveList.append(innerListItem)       
                    else:
                        newThisOutputPositiveList.append(mainListItem)
                    
                
                thisOutputPositive = newThisOutputPositiveList
                
               # print("thisOutputPositiveAFTER = ",thisOutputPositive)
                
            if len(tempOutputListNegative) > 0:
                thisOutputNegative.append(tempOutputListNegative)
                
                
                newThisOutputNegativeList = []
                
                for mainListItem in thisOutputNegative:
                    if isinstance(mainListItem, list):
                        for innerListItem in mainListItem:
                            if isinstance(innerListItem, list):
                                for thisListShouldntExist in innerListItem:
                                    newThisOutputNegativeList.append(thisListShouldntExist)
                            else:
                                newThisOutputNegativeList.append(innerListItem)       
                    else:
                        newThisOutputNegativeList.append(mainListItem)
                    
                
                thisOutputNegative = newThisOutputNegativeList
                
        
        ontOutput = self.__SearchOntologyRecursive_Placeholder(token)
        

        #print("ontOutput = ", ontOutput)
        #print(" ")
        #print("negativeInChildren = ",negativeInChildren)

        
        
        if countChildren == 0 and (ontOutput is not None):
            #print("tempOutput = ", tempOutput)
            thisOutputPositive.append(ontOutput)
        elif negativeInChildren:
            # the assumption here is that the negative is
            # attached to the top of the sub tree,
            # so in the past we did not know there was a negative list
            # so everything was in the positive list,
            # but know we knoow the negation is attached to the top of 
            # the list, this entire 'positive' list is actually
            # a negative list
            if (ontOutput is not None):
                thisOutputPositive.append(ontOutput)
                
            thisOutputNegative = thisOutputPositive
            thisOutputPositive = []
        elif countChildren > 0 and (ontOutput is not None):
            thisOutputPositive.append(ontOutput)
            
        #print("thisOutputPositiveOUTSIDE = ",thisOutputPositive)
       # print(" - - - - - - - - - - - - - - - -")
            
        return thisOutputPositive, thisOutputNegative

    def __InvestigateTreeFromRoot(self, parsedText):
        
        thisOutputPositive = []
        thisOutputNegative = []
        outputList = []
        
        for item_root in parsedText.rootList:
            tempOuputPositive, tempOutputNegative = self.__InvestigateChildNodesRecusive(item_root)
            thisOutputPositive.append(tempOuputPositive)
            thisOutputNegative.append(tempOutputNegative)
            
                    
#        print(" ")
#        print("recursive!!! = ", thisOutputPositive)
#        print(" ")
#        print("len(thisOutputPositive) = ", len(thisOutputPositive))
#        print("------------------------------------")
            
            # Flatten List (sorry Roberto!)
        #thisOutputNegative = [item for sublist in thisOutputNegative for item in sublist]
        #thisOutputPositive = [item for sublist in thisOutputPositive for item in sublist]

        
        newThisOutputPositiveList = []
                
        for mainListItem in thisOutputPositive:
            if isinstance(mainListItem, list):
                for innerListItem in mainListItem:
                    if isinstance(innerListItem, list):
                        for thisListShouldntExist in innerListItem:
                            newThisOutputPositiveList.append(thisListShouldntExist)
                    else:
                        newThisOutputPositiveList.append(innerListItem)       
            else:
                newThisOutputPositiveList.append(mainListItem)
            
        
        thisOutputPositive = newThisOutputPositiveList
        
        
        newThisOutputNegativeList = []
                
        for mainListItem in thisOutputNegative:
            if isinstance(mainListItem, list):
                for innerListItem in mainListItem:
                    if isinstance(innerListItem, list):
                        for thisListShouldntExist in innerListItem:
                            newThisOutputNegativeList.append(thisListShouldntExist)
                    else:
                        newThisOutputNegativeList.append(innerListItem)       
            else:
                newThisOutputNegativeList.append(mainListItem)
            
        
        thisOutputNegative = newThisOutputNegativeList

    
        
        
        ###############################################################
        ############## this is repetition, code it better ############
        ###############################################################

        #positive and negtive list (i think) ae filled with 
        # ontology objects so we can now just compare them 
        # to parents to see what the relationship type is 
        # (wants means cuising - user WANTS cuisine)
        # (has means ingredients - user HAS ingredients)
        
        for item in thisOutputPositive:
            #see if the item is known about in the ontology  
            #if it is the tuple is (relationship type, ontology object)
            # if not not it's (None, None)
#            
#            print(" ")
#            print(type(item))
#        
            
            if self.ontologyAnalysis.is_subclass(item,self.cuisineObject):

               ontologyObjectOutput = (self.userObject,'WantsRelationship',item)
               outputList.append(ontologyObjectOutput)
               
            elif self.ontologyAnalysis.is_subclass(item,self.ingredientObject):
                
               ontologyObjectOutput = (self.userObject, 'HasRelationship',item)
               outputList.append(ontologyObjectOutput)
               
               
        for item in thisOutputNegative:
            #see if the item is known about in the ontology
            #if it is the tuple is (relationship type, ontology object)
            # if not not it's (None, None)

            if self.ontologyAnalysis.is_subclass(item,self.cuisineObject):
 
               ontologyObjectOutput = (self.userObject,'NotWantsRelationship',item)
               outputList.append(ontologyObjectOutput)
               
            elif self.ontologyAnalysis.is_subclass(item,self.ingredientObject):
                
               ontologyObjectOutput = (self.userObject, 'NotHasRelationship',item)
               outputList.append(ontologyObjectOutput)

        
        
        return outputList



    def analyze(self, text):
        """
        This function analyzes a text by parsing and extracting relevant information from it (like verbs, nouns and
        adverbs).

        :param text:
        :return:
        """
        doc = self.parse(text)
        
        #NOT SURE YET WHAT THIS OUTPUT WILL BE
        # (currently a list)
        tempAnalysis_1 = self.InvestigateSentence(doc)
        
        # investigate tree using ontology (currently only for ingredients)
        tempAnalysis_2 = self.__InvestigateTreeFromRoot(doc)
        
        # need to sort out the ingredients lists
        tempAnalysis_1.extend(tempAnalysis_2)
        
        #state.UpdateIngredients(positiveIngredients)
        #state.UpdateNotIngredients(negativeIngredients) 
        
        tempAnalysis_1 = list(set(tempAnalysis_1))
        
        return tempAnalysis_1

    def parse(self, text):
        """
        This function parses text, and outputs a spacy 'spacy.tokens.doc.Doc'
        which is a collection of 'spacy.tokens.token.Token' objects, these
        contain many different items as can be seen in the debuggng section below

        :param text: the text to be parsed
        :return: document - 'spacy.tokens.doc.Doc' object containing parsed word tokens
        """
        return SpacyText(self.nlp(text))
        

    def ExtractNouns(self, doc):
        """
        This function picks out verbs, nouns, and adverbs from the parsed text document
        as they will be of interest later.

        :param doc: 'spacy.tokens.doc.Doc' object containing parsed word tokens
        :return: noun_token_list - list of spacy tokens of type 'noun'
                 verb_token_list - list of spacy tokens of type 'verb'
                 adverb_token_list - list of spacy tokens of type 'adverb'
        """
        print ("I think this is now redundant")
        
        noun_token_list = []
        noun_tags_list = ['NN', 'NNP', 'NNPS', 'NNS']

        verb_token_list = []
        verb_tags_list = ['VB', 'VBD', 'VBG', 'VBP', 'VBZ']

        adverb_token_list = []
        adverb_tags_list = ['RB', 'RBR', 'RBS', 'RP']

        for token in doc.Doc:
            if token.tag_ in noun_tags_list:
                noun_token_list.append(token.lower_)

            elif token.tag_ in verb_tags_list:
                verb_token_list.append(token.lower_)

            elif token.tag_ in adverb_tags_list:
                adverb_token_list.append(token.lower_)

        return noun_token_list, verb_token_list, adverb_token_list
    
    def Ontology_OLD(self, parsedText):
        """
        This function investigates the ontology to see if a given the set of 
        nouns from the parsed text are in the ontology. If so it returns 
        the words of interest and some associated ontological information
        
        inputs:
            parsedText: SpacyText Object
        
        outputs: something containing useful inforamtion...
        """
        
        nounList, _ ,_  = self.ExtractNouns(parsedText)
        outputDict = {}
        
        if False:    
            #use when we actually have an onltology
            g = rdflib.Graph()
    
            owl_file = os.path.join(os.path.dirname(__file__), '../Files/root-ontology.owl')
            g.load(owl_file)
        else:
            # if we son't have a working ontology use this as a temporary
            # ontology to allow us to test the code end to end 
            
            fruitOntology = ['tomato','orange','apple']
            vegOntology = ['olive', 'carrot', 'pea']
            meatOntology = ['chicken','beef','lamb','pork']
            dairyOntology = ['milk', 'cheese']
            miscOntology = ['egg','flour','pasta']
            
            ontologyDict = {'fruit': fruitOntology,
                            'veg': vegOntology,
                            'meat': meatOntology,
                            'dairy': dairyOntology,
                            'misc': miscOntology}
            
            for key, value in ontologyDict.items():
                for thisNoun in nounList:
                    if thisNoun in value:
                        outputDict[thisNoun] = key
                    
            return outputDict
        
        
    def InvestigateTreeFromRootTest(self, doc):
        
        return self.__InvestigateTreeFromRoot(doc)
        
        
if __name__ == "__main__":
    
    
    testText = "Hi, I have chicken but not potatoes and I would like to cook something italian."
    
    #testText = "can you suggest a recipe"
    
    from ontology import FoodOntology
    
    myOntology = ontology = FoodOntology("../resources/project_giovanni.0.1.ttl")
    
    myAnalyser = Analyzer(myOntology)
    
    doc = myAnalyser.parse(testText)
    
    myAnalyser.PrintTree(doc.Doc)
        
#    #NOT SURE YET WHAT THIS OUTPUT WILL BE
#    # (currently a list)
#    tempAnalysis_1 = myAnalyser.InvestigateSentence(doc)
#    
#    # investigate tree using ontology (currently only for ingredients)
#    tempAnalysis_2 = myAnalyser.InvestigateTreeFromRootTest(doc)
#    
#    # need to sort out the ingredients lists
#    tempAnalysis_1.extend(tempAnalysis_2)
#    
#    #tempAnalysis_1 = list(set(tempAnalysis_1))

"""
                          suggest_VB                                    
  ____________________________|____________________________________      
 |    |        |       |             have_VBP                  recipe_NN
 |    |        |       |       _________|_______________           |     
,_, can_MD -PRON-_PRP ?_.   hi_UH      ,_,    i_PRP chicken_NN    a_DT 
"""

            
                  
            

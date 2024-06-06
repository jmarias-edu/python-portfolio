import os
import re
from decimal import Decimal

def clean(word): #function to clean words
    reg = re.compile('[A-Za-z0-9]')
    cleaned = "" #variable to be returned
    for c in word.lower() : #changes the word to lowercase before cleaning
        if reg.match(c): #checks if character is alphanumeric
            cleaned = cleaned + c #appends to cleaned if alphanumeric to remove symbols
    return cleaned #returns value

def getFileData(dir): #function to get the data from text file
    dataset = [] #empty list to store initial values
    file = open(dir, "r", encoding="latin-1") #file handler
    for line in file: #loop to separate all the words per line using space
        dataset.extend(line.split(" ")) #appends to dataset list
    
    finalData = [] #final list of words after cleaning
    for word in dataset: #loop for final dataset
        finalWord = clean(word) #cleans the word
        if finalWord != '': #checks if string is empty
            finalData.append(finalWord) #appends to final list

    file.close() #closes file handler

    return finalData #returns final dataset

def getBoW(dir): #main function
    data = getFileData(dir) #gets bag of words
    bag = {} #dictionary to store words
    for word in data: # loop to add dataset to dictionary
        if word in bag.keys(): #checks if word exists in the dictionary
            bag[word]+=1 #adds tally if exists
        else: #otherwise create new key value pair
            bag[word]=1
    return bag
    


def printBoW(bag): #prints the bag of words
    keys = sorted(iter(bag.keys())) #gets list of sorted keys
    for key in keys: #iterates through entire dictionary to print
        print(key, bag[key])

def saveBoW(bag): #saves the bag of words to an output file
    keys = sorted(iter(bag.keys())) #gets list of sorted keys
    count = sum(bag.values()) #adds all values to get total number of words
    file = open("output.txt", "w") #opens file handler

    file.write("Dictionary Size: " + str(len(keys))+ "\n") #writes dictionary size
    file.write("Total Number of Words: " + str(count)+ "\n") #write total number of words
    for key in keys: #loop to add all key value pairs to output file
        newLine = str(key) + " " + str(bag[key]) + "\n"
        file.write(newLine)
    
    file.close() #closes file handler

            
def getFolderData(d): #function that gets all the data from a specified folder
    dataset = [] #main list
    for dir in sorted(os.listdir(d)): #iterates through files in directory
        file = open(d+"/"+dir, "r", encoding='latin-1') #opens files in latin encoding
        for line in file: #loop to get all words
            newLine = line.strip()
            dataset.extend(newLine.split(' '))

        file.close()
    
    finalData = [] 
    for word in dataset: #cleans the words before returning
        finalWord = clean(word)
        if finalWord != '':
            finalData.append(finalWord) 

    count = len(os.listdir(d))

    return finalData, count #returns final dataset

def getFolderBoW(d):
    data, count = getFolderData(d)
    bag = {}

    for word in data: # loop to add dataset to dictionary
        if word in bag.keys(): #checks if word exists in the dictionary
            bag[word]+=1 #adds tally if exists
        else: #otherwise create new key value pair
            bag[word]=1
    
    return bag, count

def getHamSpam(d): #returns bag of words for ham and spam
    hamBoW, hamCount = getFolderBoW(d+"/ham")
    spamBoW, spamCount = getFolderBoW(d+"/spam")

    return hamBoW, spamBoW, hamCount, spamCount
    
def computeSpamProbability(): #main function to compute
    directory = "./data/data03" #specifies dataset
    hamBoW, spamBoW, hamCount, spamCount = getHamSpam(directory)

    k = int(input("Value of k: ")) #asks for value of k
    
    spamWords = spamBoW.keys() #gets list of words in spam
    hamWords = hamBoW.keys() #gets list of words in ham

    dictSize = len(list(spamWords) + list(set(hamWords)-set(spamWords))) #gets size of dictionar

    spamProb = Decimal((spamCount+k)/(spamCount+hamCount+2*k))
    hamProb = Decimal((hamCount+k)/(spamCount+hamCount+2*k))
    totalNoSpam = sum(spamBoW.values())
    totalNoHam = sum(hamBoW.values())

    classifyCount = 1
    classifyFile = open("classify.out", "w")

    for file in sorted(os.listdir(directory+"/classify")):
        # print(file)
        bag = getBoW(directory+"/classify/"+file)
        words = bag.keys()
        wSpamProbs = Decimal(1)
        wHamProbs = Decimal(1)
        
        newWordC = 0

        for w in words:
            if w not in spamWords or w not in hamWords:
                newWordC += 1

        for w in words:
            if w in spamWords:
                p1 = Decimal((spamBoW[w]+k)/(totalNoSpam+(k*(dictSize+newWordC))))
                wSpamProbs = wSpamProbs * p1
            else:
                p1 = Decimal(k/(totalNoSpam+(k*(dictSize+newWordC))))
                wSpamProbs = wSpamProbs * p1
            if w in hamWords:
                p2 = Decimal((hamBoW[w]+k)/(totalNoHam+(k*(dictSize+newWordC))))
                wHamProbs = wHamProbs * p2
            else:
                p2 = Decimal(k/(totalNoHam+(k*(dictSize+newWordC))))
                wHamProbs = wHamProbs * p2


        msgSpamProb = Decimal(wSpamProbs*spamProb)
        msgHamProb = Decimal(wHamProbs*hamProb)
        
        finalProb = (msgSpamProb)/(msgSpamProb+msgHamProb)

        print("%03d" %classifyCount, end=" ")
        if finalProb>0.5:
            print("Spam", end=" ")
            classifyFile.write("%03d" %classifyCount)
            classifyFile.write(" SPAM "+str(finalProb)+"\n")
        else:
            print("Ham", end=" ")
            classifyFile.write("%03d" %classifyCount)
            classifyFile.write(" HAM "+str(finalProb)+"\n")
        print(finalProb)

        classifyCount+=1

    classifyFile.write("\nHAM\n"+"Dictionary Size: "+str(len(hamWords))+"\nTotal Number of Words: "+str(totalNoHam))
    classifyFile.write("\n\nSPAM\n"+"Dictionary Size: "+str(len(spamWords))+"\nTotal Number of Words: "+str(totalNoSpam)+"\n")
    classifyFile.close()

    print("\nHAM\n"+"Dictionary Size: "+str(len(hamWords))+"\nTotal Number of Words: "+str(totalNoHam))
    print("\n\nSPAM\n"+"Dictionary Size: "+str(len(spamWords))+"\nTotal Number of Words: "+str(totalNoSpam)+"\n")

computeSpamProbability()

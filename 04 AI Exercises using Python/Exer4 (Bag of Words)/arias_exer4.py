def clean(word): #function to clean words
    cleaned = "" #variable to be returned
    for c in word.lower(): #changes the word to lowercase before cleaning
        if c.isalnum(): #checks if character is alphanumeric
            cleaned = cleaned + c #appends to cleaned if alphanumeric to remove symbols
    return cleaned #returns value

def getData(): #function to get the data from text file
    dataset = [] #empty list to store initial values
    file = open("./data/003.txt", "r") #file handler
    for line in file: #loop to separate all the words per line using space
        dataset.extend(line.split(" ")) #appends to dataset list
    
    finalData = [] #final list of words after cleaning
    for word in dataset: #loop for final dataset
        finalWord = clean(word) #cleans the word
        if finalWord != '': #checks if string is empty
            finalData.append(finalWord) #appends to final list

    file.close() #closes file handler

    return finalData #returns final dataset

def printBoW(bag): #prints the bag of words
    keys = sorted(iter(bag.keys())) #gets list of sorted keys
    for key in keys: #iterates through entire dictionary to print
        print(key, bag[key])

def saveBoW(bag): #saves the bag of words to an output file
    keys = sorted(iter(bag.keys())) #gets list of sorted keys
    count = sum(bag.values()) #adds all values to get total number of words
    file = open("output.txt", "w") #opens file handler

    file.write("Dictionary Size: " + str(len(keys))+ "\n") #writes dictionary size
    file.write("Total Number of Words: " + str(count)+ "\n") #writez total number of words
    for key in keys: #loop to add all key value pairs to output file
        newLine = str(key) + " " + str(bag[key]) + "\n"
        file.write(newLine)
    
    file.close() #closes file handler

def getBoW(): #main function
    data = getData() #gets bag of words
    bag = {} #dictionary to store words
    for word in data: # loop to add dataset to dictionary
        if word in bag.keys(): #checks if word exists in the dictionary
            bag[word]+=1 #adds tally if exists
        else: #otherwise create new key value pair
            bag[word]=1
    
    printBoW(bag) #prints to terminal
    saveBoW(bag) #saves to file
            
getBoW()
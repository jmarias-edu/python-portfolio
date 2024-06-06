#Jarem Thimoty M. Arias
#2020-00782
#CMSC 170 X2L

import decimal

def loadData(): #loads data from input.txt
    f = open(r"./input.txt", "r")
    data = f.readlines() #reads all the lines
    for i in range(len(data)): #converts all the values to Decimal data type
        data[i] = data[i].strip()
        data[i] = data[i].split(" ")
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    lr = data.pop(0).pop() #gets learning rate
    t = data.pop(0).pop() #gets threshold
    b = data.pop(0).pop() #gets bias

    return lr, t, b, data

def createTable(data, bias, weights): #creates table for computation
    initTable = [[0 for j in range(len(data[0])*2+3)] for i in range(len(data))] 
    #initiates properly sized table using list comprehension

    for x in range(len(weights)): #puts initial weights for table
        initTable[0][x+len(weights)] = weights[x]
    
    for row in range(len(data)): #puts rest of the data extracted from file (x, z)
        for col in range(len(data[0])-1):
            initTable[row][col] = data[row][col]
        initTable[row][len(data[0])-1] = bias
        initTable[row][len(initTable[row])-1] = data[row][len(data[row])-1]
        
    return initTable

def checkConvergance(lastWeights, table, noOfWeights): #accessory function to check if table has converged
    for i in range(len(lastWeights)): #double for loop
        for j in range(1, len(table)):
            if lastWeights[i] != table[j][noOfWeights+i]: #checks entire column if converged, comparing to last weight
                return False
    return True

def writeToOutput(tableList, noOfWeights): #function to write to output file
    fileHandler = open("output.txt", "w") #opens file
    for table in range(len(tableList)):
        fileHandler.write("Iteration "+ str(table+1) +":\n") #writes iteration header

        firstRow = [] #list to store header contents
        for i in range(noOfWeights-1): #for loop to create appropriate number of x's
            firstRow.append("x"+ str(i))
        firstRow.append("b") #adds b to header

        for i in range(noOfWeights-1): #for loop to create appropriate number of w's
            firstRow.append("w"+ str(i))
        firstRow.extend(["wb","a","y","z"]) #adds rest of the headers

        formatTemplate = "" #string for format functions
        for col in tableList[table][0]: #adds appropriate number of placeholders
            formatTemplate = formatTemplate + "{:<8}"
        # print(formatTemplate)
        formatTemplate = formatTemplate + "\n" #adds newline

        fileHandler.write("\t\t "+formatTemplate.format(*firstRow)) #writes header to file

        for row in tableList[table]:
            roundedRow = [round(i,1) for i in row]
            fileHandler.write("\t\t "+formatTemplate.format(*roundedRow)) #writes rest of table to file

def main(): # main function
    learningRate, threshold, bias, data = loadData() # loads data from file
    tableList = [] #list to hold iterations

    noOfWeights = len(data[0]) #gets number of weights (used to access parts of the table properly)

    table = createTable(data, bias, [float(0) for i in range(noOfWeights)]) #initiates first table
    
    converge = False # boolean for while loop
    while(not converge):
        for row in range(len(table)): #iterates through whole table
            a = 0 #initial value of a
            for col in range(noOfWeights): #for loop to compute for a, accesses x and its corresponding weight
                a += table[row][col] * table[row][col+noOfWeights]
            # print(a)
            table[row][noOfWeights*2] = a #puts a in proper position in table
            y = 1 if a >= threshold else 0 #gets proper value of y
            table[row][noOfWeights*2+1] = float(y) #puts y in proper position in table

            newWeights = [] #list for new weights
            for col in range(noOfWeights): #computes for new weights
                wa = table[row][col+noOfWeights] + learningRate*table[row][col]*(table[row][noOfWeights*2+2]-table[row][noOfWeights*2+1])
                newWeights.append(wa) #adds to list

            if (not row == len(table)-1): #checks if last row, does not continue if so
                for w in range(len(newWeights)):
                    table[row+1][w+noOfWeights] = newWeights[w]

        converge = checkConvergance(newWeights, table, noOfWeights) #checks for convergence with last computed weights

        tableList.append(table) #adds table to list
        table = createTable(data, bias, newWeights) #creates new table for next iteration
        
    writeToOutput(tableList, noOfWeights)

main()
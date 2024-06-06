#Jarem Thimoty M. Arias
#2020-00782
#CMSC 170 X2L

def getTrainingData(): #function to get training data from csv
    data = []
    fp = open(r"./data/diabetes.csv", "r")
    for line in fp:
        converted = [float(x) for x in line.strip().split(",")] #gets list of floats per line
        data.append(converted) #adds to data
    fp.close()
    return data

def getInputData(): #function to get input data from in
    data = []
    fp = open(r"./data/input.in", "r")
    for line in fp:
        converted = [float(x) for x in line.strip().split(",")] #gets list of floats per line
        data.append(converted) #adds to data
    fp.close()
    return data

def writeToOutput(results): #writes results of knn to output.txt
    fp = open(r"output.txt", "w")
    for r in results:
        fp.write(str(r).replace(" ", "")[1:-1]+"\n") #writes list per line
    fp.close()

def euclidianDistance(listX, listV): #computes for euclidian distance
    output = sum([(listX[i]-listV[i])**2 for i in range(len(listX))])**0.5 #formula for euclidian distance
    return output

def main():
    k = int(input("Input number of k: ")) #gets number of k's from terminal
    trainingData = getTrainingData() #gets the training data
    inputData = getInputData() #gets the input data

    results = [] #stores the results
    for i in inputData:
        #gets list of distances and indexes using the euclidianDistance function
        distances = [[euclidianDistance(i, trainingData[d]), d] for d in range(len(trainingData))]

        #sorting a 2d list using an element within the list learned from link below
        #https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
        #gets k nearest indexes from sorted list of distances
        nearestIndexes = [x[1] for x in sorted(distances, key=lambda x:x[0])[0:k]]
        # for x in nearestIndexes:
        #     print(trainingData[x])
        # print("")
        
        #gets classes from trainingdata using the nearest indexes
        classList = [trainingData[j][len(trainingData[j])-1] for j in nearestIndexes]

        #getting mode from list without external functions learned from link below
        #https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list
        #appends mode class to input
        i.append(max(set(classList), key=classList.count))
        
        #adds results to training data and results list
        trainingData.append(i)
        results.append(i)
        
    writeToOutput(results)

main()
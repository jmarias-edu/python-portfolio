#Jarem Thimoty M. Arias
#2020-00782
#CMSC 170 - X2L

import random
import matplotlib.pyplot as plt

def getData(): #function for getting the data
    data = {}
    fp = open(r"./data/Wine.csv", "r")

    headers = fp.readline().strip().split(",") #gets the headers
    for head in headers: #creates key value pairs for the data using the headers
        data[head] = []

    for line in fp: #gets the data from the csv
        line = line.strip().split(",")
        line = [float(x) for x in line]
        for i in range(len(headers)):
            data[headers[i]].append(line[i])

    # for head in headers:
    #     print(head, str(len(data[head])))

    return headers, data #returns the data

def mean(list1): #accessory function to get the mean of a list of floats/ints
    return sum(list1)/len(list1)

def outputToFile(histX, histY, pointsX, pointsY, classes, attr1, attr2, n, iters): #file output
    fp = open(r"output.csv", "w") #writes first lines
    fp.write("Attr1: "+attr1+"\n")
    fp.write("Attr2: "+attr2+"\n")
    fp.write("n = "+str(n)+"\n")
    fp.write("Initial [")
    for x in range(n): #writes initial centroids
        fp.write(str([histX[0][x], histY[0][x]]))
        if(x<n-1):
                fp.write(", ")

    fp.write("]\n")

    ordinals = ["st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th"]

    for i in range(1, iters-1): #writes rest of the centroids
        fp.write(str(i+1)+ordinals[i%10]+" centroids [")
        for j in range(n):
            fp.write(str([histX[i][j], histY[i][j]]))
            if(j<n-1):
                fp.write(", ")
        fp.write("]\n")

    for i in range(n): #writes the final centroids and where the points belong
        fp.write("Centroid: "+str(i)+" "+ str((histX[len(histX)-1][i], histY[len(histX)-1][i]))+"\n")
        for index in range(len(classes)):
            if classes[index] == i:
                fp.write(str([pointsX[index], pointsY[index]])+"\n")

def main(): #main function
    headers, data = getData()
    # col1 = "Alcohol"
    # col2 = "Malic_Acid"
    # k = 2

    print("==Choose first attribute==") #input for 1st attribute
    for i in range(len(headers)):
        print(str(i)+") "+headers[i])
    col1 = headers[int(input("Choose 1st attribute: "))]

    print("\n==Choose second attribute==") #input for 2nd attribute
    for i in range(len(headers)):
        if headers[i]==col1: continue
        print(str(i)+") "+headers[i])
    col2 = headers[int(input("Choose 2nd attribute: "))]

    k = int(input("Choose k (Max 10): ")) #input for k

    randomIndex = [random.randint(0, len(data[col1])-1) for x in range(k)] #gets k number of random points
    pointsX = data[col1] #gets x's of attribute 1
    pointsY = data[col2] #gets y's of attribute 2
    centroidX = [pointsX[x] for x in randomIndex] #gets points of random centroids
    centroidY = [pointsY[x] for x in randomIndex]
    prevX = [0 for x in range(k)] #initiates list for previous centroids
    prevY = [0 for x in range(k)]

    centroidHistX = [centroidX] #adds initial centroids to history
    centroidHistY = [centroidY]

    counter = 0 #counter for printing
    while True:
        counter += 1 #increments counter
        #computes the distances of each point from all the centroids
        distances = [[((pointsX[i]-centroidX[j])**2 + (pointsY[i]-centroidY[j])**2)**0.5 for i in range(len(pointsX))] for j in range(len(centroidX))]
        classes = []
        #gets the classes/membership of each point
        for i in range(len(pointsX)):
            pointDist = [distances[j][i] for j in range(k)]
            classes.append(pointDist.index(min(pointDist)))

        # print(classes)

        #break statement if current centroid does not change anymore
        if prevX == centroidX and prevY == centroidY:
            break

        #changes previous centroid
        prevX = centroidX
        prevY = centroidY

        # print("Before: ")
        # print(centroidX)
        # print(centroidY)

        #initiates empty list for centroids for getting mean
        centroidX = [[] for x in range(k)]
        centroidY = [[] for x in range(k)]

        #adds the points that belong to each 
        for i in range(len(classes)):
            centroidX[classes[i]].append(pointsX[i])
            centroidY[classes[i]].append(pointsY[i])
        
        #gets the new centroids
        centroidX = [mean(centroidX[i]) for i in range(k)]
        centroidY = [mean(centroidY[i]) for i in range(k)]

        #adds centroids to history
        centroidHistX.append(centroidX)
        centroidHistY.append(centroidY)

        # print("After: ")
        # print(centroidX)
        # print(centroidY)

    # print(classes)
    
    #creates scatter plot output
    colors = ["red","green","blue","yellow","pink","black","orange","purple","beige","brown"]
    for i in range(len(pointsX)):
        plt.scatter(pointsX[i], pointsY[i], color=colors[classes[i]])
    plt.savefig("output.png")
    # plt.show()

    # print(len(centroidHistX))
    # print(len(centroidHistY))

    outputToFile(centroidHistX, centroidHistY, pointsX, pointsY, classes, col1, col2, k, counter)
    
main()
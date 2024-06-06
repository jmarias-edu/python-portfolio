def getData():
    data = {}
    fp = open(r"hmm.in", "r")
    data["#str"] = int(fp.readline())
    data["strings"] = []
    for i in range(data["#str"]):
        data["strings"].append(fp.readline().strip())

    posval = fp.readline().strip().split(" ")
    posobs = fp.readline().strip().split(" ")

    data["obs"] = {}
    for j in posval:
        for i in posobs:
            data["obs"][i+j] = 0

    pvalESFS = fp.readline().strip().split(" ")
    pvalESFS = [float(x) for x in pvalESFS]

    data["obs"]["ES"] = pvalESFS[0]
    data["obs"]["FS"] = pvalESFS[1]

    pvalETFT = fp.readline().strip().split(" ")
    pvalETFT = [float(x) for x in pvalETFT]

    data["obs"]["ET"] = pvalETFT[0]
    data["obs"]["FT"] = pvalETFT[1]

    data["#cases"] = int(fp.readline())
    data["cases"] = []
    for i in range(data["#cases"]):
        data["cases"].append(fp.readline().strip().split(" given "))
        data["cases"][i].append(int(data["cases"][i][0][1]))
        data["cases"][i][0] = data["cases"][i][0][0]
        data["cases"][i][1] = data["cases"][i][1][0]

    print(data)

    return(data)

def getTransProbs(string):
    prev = ""
    count = {}
    transitions = {}

    for x in range(len(string)):
        if string[x] in count.keys():
            count[string[x]] += 1
        else:
            count[string[x]] = 1

        if prev+string[x] in transitions.keys():
            transitions[prev+string[x]] += 1
        else:
            transitions[prev+string[x]] = 1


        prev = string[x]

    count[string[len(string)-1]] -= 1
    # count["T"] = 2
    # count["S"] = 7
    transitions.pop(string[0])
    
    # print("count:",count)
    # print("transitions:",transitions)

    for key in transitions.keys():
        transitions[key] = transitions[key]/count[key[0]]

    return(transitions)

def outputToFile(strings, queries, results):
    fp = open(r"hmm.out", "w")
    for i in range(len(strings)):
        fp.write(strings[i]+"\n")
        for j in range(len(queries)):
            fp.write(queries[j][0]+str(queries[j][2])+" given "+queries[j][1]+str(queries[j][2])+" = "+ str(round(results[i][j], 4))+"\n")

def bayesRuleComp(case, obsval, iterS):
    m1 = obsval[case[1]+case[0]]
    m2 = iterS if case[0]=="S" else 1-iterS
    d = obsval[case[1]+"S"]*iterS + obsval[case[1]+"T"]*(1-iterS)
    answer = (m1*m2)/d
    # print("answer:", answer)
    return answer

def totalProbS(transProbs, prevS):
    return transProbs["SS"]*prevS + transProbs["TS"]*(1-prevS)

def main():
    data = getData()
    maxIter = max([data["cases"][x][2] for x in range(data["#cases"])])
    # print(maxIter)
    finalResults = []

    for i in range(data["#str"]):
        HistS = [1 if data["strings"][i][0] == "S" else 0]
        # HistT = [1-HistS[0]]
        transProbs = getTransProbs(data["strings"][i])
        # print(transProbs)
        for x in range(maxIter):
            HistS.append(totalProbS(transProbs, HistS[len(HistS)-1]))
            # HistT.append(1-HistS[len(HistS)-1])
        # print(HistS)
        # print(HistT)
        results = []
        for x in range(data["#cases"]):
            results.append(bayesRuleComp(data["cases"][x], data["obs"], HistS[data["cases"][x][2]]))
        finalResults.append(results)

    outputToFile(data["strings"], data["cases"], finalResults)

main()
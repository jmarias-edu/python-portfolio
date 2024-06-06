from tkinter import *
from functools import partial
import tkinter.font as font
import copy
from tkinter import filedialog
import time

class EightPuzzleGame(Tk): # Tkinter Classes learned from tkinter documentation http://tkdocs.com/tutorial
    def __init__(self):
        super(EightPuzzleGame, self).__init__()
        
        self.title("8 Puzzle Game")
        self.minsize(300,340)
        self.resizable(0,0)
         
        self.frame = Frame(self)
        self.frame.grid(column=0, row=0, sticky=(N,W,E,S))

        self.buttonFont = font.Font(size=15, family="Helvetica")

        self.pixelSize = PhotoImage(width=1, height=1)

        self.fileName = "puzzle.in"

        self.puzzleData = self.loadPuzzleData(self.fileName)

        self.buttons = self.createButtons(self.frame)

        self.dropDownChoice = StringVar(self)
        self.dropDownChoice.set("BFS")
        self.dropDownList = OptionMenu(self.frame, self.dropDownChoice, "BFS", "DFS", "A*")
        self.dropDownList.grid(column=2, row=4)
        
        if(self.checkIfSolvable(self.puzzleData)):
            print("Solvable!")
            self.solveLabel = Label(self.frame, text="Solvability:\nSolvable!", bg="green")
            self.solveButton = Button(self.frame, text="Solution", command=partial(self.onClickSolve, self.dropDownChoice), font=self.buttonFont)
        else:
            print("Not Solvable")
            self.solveLabel = Label(self.frame, text="Solvability:\nNot Solvable!", bg="red")
            self.solveButton = Button(self.frame, text="Solution", command=partial(self.onClickSolve, self.dropDownChoice), font=self.buttonFont, state="disabled")

        self.solveLabel.grid(column=1, row=4)
        self.solveButton.grid(column=3, row=4)

        self.newFile = Button(self.frame, text="Open Puzzle", command=self.loadNewFile)
        self.newFile.grid(column=2, row=0)

        self.solution = []
        self.pathCost = 0
        self.winState = {}

    def onClickSolve(self, c): #function for using the brute force algorithms
        choice = c.get() #gets choice of algorithm
        print(choice)

        self.puzzleData = self.loadPuzzleData(self.fileName) #reloads the puzzle.in data
        self.buttons = self.createButtons(self.frame)
        self.pathCost = 0

        for x in range(9): #removes functionality of the buttons
            self.buttons[x]["command"] = self.onClickDud

        self.dropDownList["state"] = "disabled" #disables the dropdown list
        
        self.solveButton["state"] = "disabled" #temporarily disables the button until algo is finished running
        self.solveButton["text"] = "Next"

        puzzleDataCopy = self.puzzleData[:] #copies puzzle data

        startTime = time.time()

        if choice == "BFS": #inputs puzzleData into brute force algorithms
            self.winState = self.BFSearch(puzzleDataCopy)
        elif choice == "DFS":
            self.winState = self.DFSearch(puzzleDataCopy)
        elif choice == "A*":
            self.winState = self.ASSearch(puzzleDataCopy)

        runTime = time.time() - startTime
        print("The runtime was:", runTime)

        self.solution = self.winState["lastActions"] #gets actions for solution

        self.writeToOut() # writes the solution to puzzle.out
        
        self.printState(self.winState)
        
        self.solveButton["command"] = partial(self.onClickNext) #changes solve button to 
        self.solveButton["state"] = "normal"

    def onClickDud(self): #dud function for solution portion
        pass
        
    def onClickNext(self): #function for functionality of next button
        print("next was pressed")

        for x in self.buttons: #resets color of buttons
            x['bg'] = 'lightGrey'

        m, zeroRow, zeroCol, d = self.getMovable(self.puzzleData) #gets coordinate of button to move

        nextAction = self.solution.pop(0)

        if nextAction== "U":
            toMoveR = zeroRow - 1
            toMoveC = zeroCol
        elif nextAction=="L":
            toMoveR = zeroRow
            toMoveC = zeroCol - 1
        elif nextAction=="R":
            toMoveR = zeroRow
            toMoveC = zeroCol + 1
        elif nextAction=="D":
            toMoveR = zeroRow + 1
            toMoveC = zeroCol

        self.onClick(toMoveR*3+toMoveC) #moves button and changes color to highlight
        self.buttons[zeroRow*3+zeroCol]['bg'] = 'gray'

    def loadPuzzleData(s, fn):
        f = open(fn, "r") #file handler
        data = f.readlines()
        
        finalData = []
        for i in range(3): #loop to put data from file into proper format
            finalData.append(data[i].split(" "))
            if i < 2:
                finalData[i][2] = finalData[i][2][0:1]
            for j in range(3):
                finalData[i][j] = int(finalData[i][j])
        #print(finalData)
        f.close()
        return finalData

    def loadNewFile(self):
        filename = filedialog.askopenfilename(initialdir = "./", title = "Select a File", filetypes = (("Puzzle files","*.in*"),("all files","*.*")))
        if(filename==()):
            print("Did not select a file")
            return
        self.fileName = filename

        
        self.puzzleData = self.loadPuzzleData(filename)

        self.buttons = self.createButtons(self.frame)

        if(self.checkIfSolvable(self.puzzleData)):
            print("Solvable!")
            self.solveLabel = Label(self.frame, text="Solvability:\nSolvable!", bg="green")
            self.solveButton = Button(self.frame, text="Solution", command=partial(self.onClickSolve, self.dropDownChoice), font=self.buttonFont)
        else:
            print("Not Solvable")
            self.solveLabel = Label(self.frame, text="Solvability:\nNot Solvable!", bg="red")
            self.solveButton = Button(self.frame, text="Solution", command=partial(self.onClickSolve, self.dropDownChoice), font=self.buttonFont, state="disabled")

        self.solveLabel.grid(column=1, row=4)
        self.solveButton.grid(column=3, row=4)

    def checkIfWin(self, pd): #checks if won
        winPattern = [[1,2,3],[4,5,6],[7,8,0]]
        for i in range(3):
            for j in range(3):
                if winPattern[i][j] != pd[i][j]:
                    return False
        return True

    def checkIfSolvable(s, pd): #checks if puzzle is solvable through the parity of the inverses learned from: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
        invCount = 0 
        flatpd = []
        for r in pd: #flattens the list
            for c in r:
                flatpd.append(c)

        for i in range(9): #Loop to count number of inverses
            for j in range(i+1, 9):
                if flatpd[i] != 0 and flatpd[j] != 0 and flatpd[i] > flatpd[j]:
                    invCount+=1

        #print(invCount)
        if invCount%2 == 0: #returns if puzzle is solvable or not
            return True
        return False

    def win(self): #function to trigger win
        for x in range(9):
            self.buttons[x]["state"] = "disabled"
            self.buttons[x]["text"] = "YOU WIN!"
        self.solveButton["state"] = "disabled"
        self.showPrompt()
    
    def showPrompt(self): #prompt for when game ends
        top = Toplevel(self)
        top.geometry("200x50")
        top.title("End of Game!")
        text = Label(top, text=("Path Cost: "+str(self.pathCost)))
        
        exitBtn = Button(top, text="exit", command=self.destroy)

        text.pack()
        exitBtn.pack()

    def writeToOut(self): #writes result of brute force algorithm to puzzle.out
        f = open("puzzle.out", "w")
        #print(self.solution)
        for x in self.solution:
            #print("Writing: ", x)
            f.write(x+" ")

    def printPuzzle(self): #prints puzzle data to the terminal using a double for loop
        print("Current State of Puzzle:")
        for i in range(3):
            for j in range(3):
                print(self.puzzleData[i][j], end="")
            print("")

    def printPuzzle1(self, p): #prints puzzle data to the terminal using a double for loop
        print("Current State of Puzzle:")
        for i in range(3):
            for j in range(3):
                print(p[i][j], end="")
            print("")

    def onClick(self, btn): #function that handles button clicks
        pressedButton = self.buttons[btn]
        movable, zeroRow, zeroCol, directions = self.getMovable(self.puzzleData)

        zeroButton = self.buttons[zeroRow*3+zeroCol]
        
        print("========")
        print("Clicked btn: ", btn, "btn value: ", pressedButton["text"])

        if btn not in movable: #checks if button is movable
            print("This value cannot be moved")
            return

        pressedBtnVal = int(pressedButton["text"])

        zeroButton["text"] = str(pressedBtnVal) #Swaps the values of the zero button and pressed button
        zeroButton["state"] = "normal"
        zeroButton["borderwidth"] = 1
        pressedButton["text"] = ""
        pressedButton["state"] = "disabled"
        pressedButton["borderwidth"] = 0

        self.puzzleData[zeroRow][zeroCol] = pressedBtnVal #Swaps the values in the puzzleData attribute
        self.puzzleData[btn//3][btn%3] = 0
        
        self.printPuzzle()

        self.pathCost += 1

        if (self.checkIfWin(self.puzzleData)): #checks if win
            print("Win!")
            self.win()

    def createButtons(self, f): #function that creates the buttons
        buttons = []
        for i in range(3):
            for j in range(3): #https://www.delftstack.com/howto/python-tkinter/how-to-change-the-tkinter-button-size/
                if self.puzzleData[i][j] != 0:
                    btn = Button(f, text=str(self.puzzleData[i][j]), image=self.pixelSize, width=100, height=100, compound="bottom",
                                command=partial(self.onClick, i*3+j), font=self.buttonFont) #https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop
                else:
                    btn = Button(f, text="", image=self.pixelSize, width=100, height=100, compound="bottom",
                                command=partial(self.onClick, i*3+j), state="disabled", borderwidth=0, font=self.buttonFont) #https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop
                btn.grid(column=j+1, row=i+1)
                buttons.append(btn)

        return buttons

    def getMovable(self, p): #Function to see what buttons are movable, also returns coordinate of button with 0
        movable = []
        directions = []
        for i in range(3):
            for j in range(3):
                if p[i][j] == 0:
                    if i == 0 and j == 0:
                        movable.extend((1,3))
                        directions.extend(("R", "D")) #Added functionality to determine which directions are movable
                    elif i == 0 and j == 1:
                        movable.extend((0,2,4))
                        directions.extend(("R","D","L"))
                    elif i == 0 and j == 2:
                        movable.extend((1,5))
                        directions.extend(("D","L"))
                    elif i == 1 and j == 0:
                        movable.extend((0,4,6))
                        directions.extend(("U","R","D"))
                    elif i == 1 and j == 1:
                        movable.extend((1,3,5,7))
                        directions.extend(("U","R","D","L"))
                    elif i == 1 and j == 2:
                        movable.extend((2,4,8))
                        directions.extend(("U","D","L"))
                    elif i == 2 and j == 0:
                        movable.extend((3,7))
                        directions.extend(("U","R"))
                    elif i == 2 and j == 1:
                        movable.extend((4,6,8))
                        directions.extend(("U","R","L"))
                    elif i == 2 and j == 2:
                        movable.extend((5,7))
                        directions.extend(("U","L"))

                    return movable, i, j, directions

    def printState(self, state): #prints state of state
        print("====State Info====")
        self.printPuzzle1(state["puzzleData"])
        print("Action List:", state["lastActions"])
        print("PathCost:",len(state["lastActions"]))
        print("Possible Next Actions", state["actions"])
        

    def actionResult(self, initialState, action): #outputs the result of an action to a state
        newState = copy.deepcopy(initialState)
        movable, zeroRow, zeroCol, directions = self.getMovable(newState["puzzleData"])
        
        if action not in directions:
            print("Action not possible")
            return newState
        
        if action== "U":
            toMoveR = zeroRow - 1
            toMoveC = zeroCol
        elif action=="L":
            toMoveR = zeroRow
            toMoveC = zeroCol - 1
        elif action=="R":
            toMoveR = zeroRow
            toMoveC = zeroCol + 1
        elif action=="D":
            toMoveR = zeroRow + 1
            toMoveC = zeroCol

        newState['puzzleData'][zeroRow][zeroCol] = newState['puzzleData'][toMoveR][toMoveC]
        newState['puzzleData'][toMoveR][toMoveC] = 0
        newState['lastActions'].append(action)

        movable1, zeroRow1, zeroCol1, directions1 = self.getMovable(newState['puzzleData'])
        
        newState['actions'] = directions1[:]

        return newState

    def checkIfIn(self, p, l): #checks if state of puzzle already exists
        for puzzle in l:
            result = self.checkIfInHelper(p, puzzle["puzzleData"])
            if(result):
                return True
        return False

    def checkIfIn1(self, p, l): #checks if state of puzzle already exists
        curPuzzle = {}
        for puzzle in l:
            curPuzzle = puzzle
            result = self.checkIfInHelper(p, puzzle["puzzleData"])
            if(result):
                return True, curPuzzle
        return False, curPuzzle

    def checkIfInHelper(self, p1, p2): #Helper function for checkIfIn (Checks for equality of puzzles)
        for i in range(3):
            for j in range(3):
                if p1[i][j] != p2[i][j]:
                    return False
        return True

    def BFSearch(self, initPuzzle): #Breadth First Search Algorithm
        exploredNumber = 0

        m, zr, zc, d = self.getMovable(initPuzzle) #Initializes frontier
        frontier = [{"puzzleData": initPuzzle[:], "lastActions": [], "actions": d}]
        exploredPuzzles = []

        exploredPuzzles.append(frontier[0]) #appends first state into explored

        print("Initial State:")
        self.printState(frontier[0])

        while(len(frontier)>0): #while loop for BFSearch
            currentState = frontier.pop(0) #dequeues state from frontier
            exploredPuzzles.append(currentState)
            exploredNumber += 1
            print(exploredNumber)
            if(self.checkIfWin(currentState['puzzleData'])):
                return currentState
            else:
                for x in currentState["actions"]:
                    result = self.actionResult(currentState, x)
                    if not self.checkIfIn(result['puzzleData'], exploredPuzzles) and not self.checkIfIn(result['puzzleData'], frontier):
                        frontier.append(result) #queues new state into frontier
    
    def DFSearch(self, initPuzzle): #Almost the same as BFS
        exploredNumber = 0

        m, zr, zc, d = self.getMovable(initPuzzle) #Initializes frontier
        frontier = [{"puzzleData": initPuzzle[:], "lastActions": [], "actions": d}]
        exploredPuzzles = []

        exploredPuzzles.append(frontier[0]) #appends first state into explored

        print("Initial State:")
        self.printState(frontier[0])

        while(len(frontier)>0): #while loop for BFSearch
            currentState = frontier.pop() #dequeues state from frontier
            exploredPuzzles.append(currentState)
            exploredNumber += 1
            print(exploredNumber)
            if(self.checkIfWin(currentState['puzzleData'])):
                return currentState
            else:
                for x in currentState["actions"]:
                    result = self.actionResult(currentState, x)
                    if not self.checkIfIn(result['puzzleData'], exploredPuzzles) and not self.checkIfIn(result['puzzleData'], frontier):
                        frontier.append(result) #queues new state into frontier


    def manhattanDistance(self, state):
        #compute manhattan distance
        flatpd = []
        for r in state["puzzleData"]: #flattens the list
            for c in r:
                flatpd.append(c)

        endGoal = (1,2,3,4,5,6,7,8,0)
        distance = 0
        for i in range(9):
            for j in range(9):
                if(endGoal[i]==flatpd[j] and (endGoal[i]!=0)):
                    distance += (abs(i//3-j//3)+abs(i%3-j%3))
        return distance

    def getEstimatedCost(self, state):
        cost = 0
        cost += len(state["lastActions"])
        cost += self.manhattanDistance(state)
        return cost

    def returnBest(self, l):
        currentBestState = l[0]
        bestStateIndex = 0
        for x in range(1,len(l)):
            if (self.getEstimatedCost(currentBestState)>self.getEstimatedCost(l[x])):
                currentBestState = l[x]
                bestStateIndex = x
        bestState = l.pop(bestStateIndex)
        return bestState

    def ASSearch(self, initPuzzle):
        exploredNumber = 0

        m, zr, zc, d = self.getMovable(initPuzzle) #Initializes frontier
        frontier = [{"puzzleData": initPuzzle[:], "lastActions": [], "actions": d}]
        exploredPuzzles = []

        #exploredPuzzles.append(frontier[0]) #appends first state into explored

        print("Initial State:")
        self.printState(frontier[0])

        while(len(frontier)>0): #while loop for BFSearch
            currentState = self.returnBest(frontier) #dequeues state from frontier
            exploredPuzzles.append(currentState)
            exploredNumber += 1
            print(exploredNumber)
            if(self.checkIfWin(currentState['puzzleData'])):
                print("Final Size:",len(exploredPuzzles))
                return currentState
            else:
                for x in currentState["actions"]:
                    result = self.actionResult(currentState, x)
                    inFrontier, puzzleIfIn = self.checkIfIn1(result['puzzleData'], frontier)
                    
                    if not inFrontier and not self.checkIfIn(result['puzzleData'], exploredPuzzles):
                        frontier.append(result) #queues new state into frontier
                    elif inFrontier and (len(puzzleIfIn["lastActions"])>len(result["lastActions"])):
                        print("Result:", len(result["lastActions"]))
                        print("InFrontier:", len(puzzleIfIn["lastActions"]))
                        puzzleIfIn["lastActions"] = result["lastActions"]

root = EightPuzzleGame()
root.mainloop()

from asyncio.windows_events import NULL
from tkinter import *
from functools import partial
import tkinter.font as font
import copy

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

        self.puzzleData = self.loadPuzzleData()

        self.buttons = self.createButtons(self.frame)
        
        if(self.checkIfSolvable(self.puzzleData)):
            print("Solvable!")
            self.solveLabel = Label(self.frame, text="Solvability:\nSolvable!", bg="green")
        else:
            print("Not Solvable")
            self.solveLabel = Label(self.frame, text="Solvability:\nNot Solvable!", bg="red")

        self.solveLabel.grid(column=2, row=4)

        puzzleDataCopy = self.puzzleData[:]
        BFSWinState, BFSPathCost = self.BFSearch(puzzleDataCopy)
        self.printState(BFSWinState, BFSPathCost)
        
        #print(self.buttons)

    def loadPuzzleData(s):
        f = open(r"puzzle.in", "r") #file handler
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
        

    def checkIfWin(s, pd): #checks if won
        winPattern = [[1,2,3],[4,5,6],[7,8,0]]
        if pd == winPattern:
            return True
        return False

    def checkIfWin1(self, pd): #checks if won
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

        if (self.checkIfWin1(self.puzzleData)):
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
                        directions.extend(("R", "D"))
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

    def printState(self, state, action):
        print("====State Info====")
        self.printPuzzle1(state["puzzleData"])
        print("Zero Row:", state["zeroRow"])
        print("Zero Col:", state["zeroCol"])
        print("Action to take:", action)
        print("Action List:", state["lastActions"])
        print("Possible Next Actions", state["actions"])
        

    def actionResult(self, initialState, action):
        
        newState = copy.deepcopy(initialState)
        #self.printState(newState, action)
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
        newState['zeroRow'] = toMoveR
        newState['zeroCol'] = toMoveC
        newState['lastActions'].append(action)

        movable1, zeroRow1, zeroCol1, directions1 = self.getMovable(newState['puzzleData'])
        
        newState['actions'] = directions1[:]

        return newState

    def checkIfIn(self, p, l):
        for puzzle in l:
            result = self.checkIfInHelper(p, puzzle)
            if(result):
                return True
        return False

    def checkIfInHelper(self, p1, p2):
        for i in range(3):
            for j in range(3):
                if p1[i][j] != p2[i][j]:
                    return False
        return True

    def BFSearch(self, initPuzzle):
        pathcost = 0

        m, zr, zc, d = self.getMovable(initPuzzle)
        frontier = [{"puzzleData": initPuzzle[:], "zeroRow": zr, "zeroCol": zc, "lastActions": [], "actions": d}]
        exploredPuzzles = []
        frontierPuzzles = []
        #frontier = [{"puzzleData": [[1,2,3],[4,5,6],[0,7,8]], "zeroRow": zr, "zeroCol": zc, "lastActions": [], "actions": d}]

        print("Initial State:")
        self.printState(frontier[0], "")

        while(len(frontier)>0):
            currentState = frontier.pop()
            exploredPuzzles.append(currentState["puzzleData"])
            pathcost += 1
            print(pathcost)
            if(self.checkIfWin1(currentState['puzzleData'])):
                return currentState, pathcost
            else:
                for x in currentState["actions"]:
                    result = self.actionResult(currentState, x)
                    if not self.checkIfIn(result['puzzleData'], exploredPuzzles) and not self.checkIfIn(result['puzzleData'], frontierPuzzles):
                        frontier.append(result)
                        frontierPuzzles.append(result['puzzleData'])

    def actionResult1(self, initialState, action):
        
        newState = copy.deepcopy(initialState)
        #self.printState(newState, action)
        movable, zeroRow, zeroCol, directions = self.getMovable(newState["puzzleData"])
        
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
        newState['zeroRow'] = toMoveR
        newState['zeroCol'] = toMoveC
        newState['lastActions'].append(action)

        movable1, zeroRow1, zeroCol1, directions1 = self.getMovable(newState['puzzleData'])
        
        newStates = []

        for a in directions1:
            temp = copy.deepcopy(newState)
            temp["actions"] = a
            #print(temp)
            newStates.append(temp)

        print(newStates)

        return newStates

    def BFSearch1(self, initPuzzle):
        m, zr, zc, d = self.getMovable(initPuzzle)
        frontier = [{"puzzleData": initPuzzle[:], "zeroRow": zr, "zeroCol": zc, "lastActions": [], "actions": i} for i in d]
        explored = []
        pathsExplored = 0

        print("Initial State:")
        self.printState(frontier[0], "")

        while(len(frontier)>0):
            currentState = frontier.pop(0)
            explored.append(currentState)
            pathsExplored +=1

            if(self.checkIfWin1(currentState['puzzleData'])):
                print(len(explored))
                return currentState, pathsExplored
            else:
                for x in currentState["actions"]:
                    result = self.actionResult1(currentState, x)
                    for y in result:
                        if (y not in explored) or (y not in frontier):
                            frontier.append(y)

    def DFSearch(self, initialState):
        pass

    def printActions(self, f, a):
        for x in range(len(f)):
            self.printState(f[x], a)

root = EightPuzzleGame()
root.mainloop()
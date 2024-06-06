from tkinter import *
from functools import partial
import tkinter.font as font

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

    def onClick(self, btn): #function that handles button clicks
        pressedButton = self.buttons[btn]
        movable, zeroRow, zeroCol = self.getMovable(self.puzzleData)

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

        if (self.checkIfWin(self.puzzleData)):
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
        for i in range(3):
            for j in range(3):
                if p[i][j] == 0:
                    if i == 0 and j == 0:
                        movable.extend((1,3))
                    elif i == 0 and j == 1:
                        movable.extend((0,2,4))
                    elif i == 0 and j == 2:
                        movable.extend((1,5))
                    elif i == 1 and j == 0:
                        movable.extend((0,4,6))
                    elif i == 1 and j == 1:
                        movable.extend((1,3,5,7))
                    elif i == 1 and j == 2:
                        movable.extend((2,4,8))
                    elif i == 2 and j == 0:
                        movable.extend((3,7))
                    elif i == 2 and j == 1:
                        movable.extend((4,6,8))
                    elif i == 2 and j == 2:
                        movable.extend((5,7))

                    return movable, i, j

root = EightPuzzleGame()
root.mainloop()
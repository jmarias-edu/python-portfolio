from tkinter import *
import random
from functools import partial

#function to create the data for the puzzle
def createPuzzle():
    puzzleData = [x for x in range(9)] #creates the shuffled numbers for the puzzle
    random.shuffle(puzzleData)

    puzzle = [] # main list to keep data in

    for i in range(3): # for loop to turn data into 2d array
        row = []
        for j in range(3):
            row.append(puzzleData[(i*3)+j])
        puzzle.append(row)

    return puzzle #returns finished puzzle data

def printPuzzle(p): #prints puzzle data to the terminal using a double for loop
    print("Current State of Puzzle:")
    for i in range(3):
        for j in range(3):
            print(p[i][j], end="")
        print("")

puzzleData = createPuzzle()
printPuzzle(puzzleData)

root = Tk() #http://tkdocs.com/tutorial/firstexample.html
root.title("Eight-Puzzle Game")
root.minsize(600,600)
root.resizable(0,0)

frame = Frame(root)
frame.grid(column=0, row=0, sticky=(N,W,E,S))

pixelSize = PhotoImage(width=1, height=1)

buttons = []

def getMovable(p):
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

def onclick(x):
    #Get Value of button, check if 0 is adjacent, then switch value if adjacent
  
    pressedBtn = buttons[x]
    print("Button Pressed: ", x+1, "Button Value:", pressedBtn["text"])

    movable, zeroRow, zeroCol = getMovable(puzzleData)
    print("Movable: ", movable)

    if x not in movable:
        print("This value cannot be moved")
        return

    value = int(pressedBtn["text"])

    puzzleData[x//3][x%3] = 0
    
    puzzleData[zeroRow][zeroCol] = value

    printPuzzle(puzzleData)
    
    pressedBtn["text"] = 0 #https://stackoverflow.com/questions/32615440/python-3-tkinter-how-to-update-button-text
    buttons[zeroRow*3+zeroCol]["text"] = str(value)
    
    print("is movable")

for i in range(3):
    for j in range(3): #https://www.delftstack.com/howto/python-tkinter/how-to-change-the-tkinter-button-size/
        btn = Button(frame, text=str(puzzleData[i][j]), image=pixelSize, width=200, height=200, compound="c", command=partial(onclick, i*3+j)) #https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop
        btn.grid(column=j+1, row=i+1)
        buttons.append(btn)

#print(buttons)

root.mainloop()

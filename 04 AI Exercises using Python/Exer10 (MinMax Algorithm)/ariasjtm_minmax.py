from tkinter import *
from functools import partial
import tkinter.font as font
import random

#constants used
NEG_INF = -999999999
POS_INF = 999999999

#global variable for choice
playerChoice = " "

class TicTacToe(Tk): # Tkinter Classes learned from tkinter documentation http://tkdocs.com/tutorial
    def __init__(self):
        super(TicTacToe, self).__init__()
        global playerChoice
        
        self.title("Tic Tac Toe")
        self.minsize(300,340)
        self.resizable(0,0)
        self.turn = playerChoice
        self.aiTurn = "X" if self.turn == "O" else "O"
        self.winner = ""

        self.boardData = [" " for x in range(9)]
        
        self.frame = Frame(self)
        self.frame.grid(column=0, row=0, sticky=(N,W,E,S))

        self.buttonFont = font.Font(size=15, family="Helvetica")

        self.pixelSize = PhotoImage(width=1, height=1)

        self.buttons = self.createButtons(self.frame)

        #first move if ai is X
        if self.aiTurn == "X":
            # aiMove = self.randomAgent(self.aiTurn, self.boardData) #Temporary random agent for 
            aiMove = self.minMaxAgent(True, self.boardData[:])["cell"]
            self.buttons[aiMove]["text"] = self.aiTurn
            self.boardData[aiMove] = self.aiTurn
            self.buttons[aiMove]["state"] = "disabled"
        

    def checkIfWin(self): #checks if won

        for i in range(3): #checks horizontally
            if len(set(self.boardData[i*3:i*3+3])) == 1 and self.boardData[i*3] != " ":
                return self.boardData[i*3]

        for i in range(3): #checks vertically
            if len(set(self.boardData[i::3])) == 1 and self.boardData[i] != " ":
                return self.boardData[i]

        if(len(set(self.boardData[::4]))==1 and self.boardData[0] != " "): #checks diagonally left
            return self.boardData[0]

        if(len(set(self.boardData[2:-2:2]))==1 and self.boardData[2] != " "): #checks diagonally right
            return self.boardData[2]

        if len([i for i in self.boardData if i == " "]) == 0: #Checks if draw
            return "D"
        
        return " "

    def win(self, result): #win actions
        self.winner = result
        print(result)
        print(self.boardData)
        self.showPrompt()

    def showPrompt(self): #prompt for when game ends
        top = Toplevel(self)
        top.geometry("200x50")
        top.title("End of Game!")

        if self.winner in ("X", "O"):
            text = Label(top, text=(self.winner+" has won!"))
        else:
            text = Label(top, text=("Its a draw!"))
        
        exitBtn = Button(top, text="exit", command=self.destroy)

        text.pack()
        exitBtn.pack()

    def onClick(self, btn): #function that handles button clicks

        #Player move
        if self.turn == "X":
            self.buttons[btn]["text"] = "X"
            self.boardData[btn] = "X"
            self.buttons[btn]["state"] = "disabled"

        elif self.turn == "O":
            self.buttons[btn]["text"] = "O"
            self.boardData[btn] = "O"
            self.buttons[btn]["state"] = "disabled"

        #Checks if move wins
        result = self.checkIfWin()
        if result != " ":
            self.win(result)
            return

        #Ai Move
        # aiMove = self.randomAgent(self.aiTurn, self.boardData)
        aiMove = self.minMaxAgent(True, self.boardData[:])
        print(aiMove["cell"])
        print(aiMove["score"])
        if self.aiTurn == "X":
            self.buttons[aiMove["cell"]]["text"] = "X"
            self.boardData[aiMove["cell"]] = "X"
            self.buttons[aiMove["cell"]]["state"] = "disabled"
        elif self.aiTurn == "O":
            self.buttons[aiMove["cell"]]["text"] = "O"
            self.boardData[aiMove["cell"]] = "O"
            self.buttons[aiMove["cell"]]["state"] = "disabled"
        
        #Checks if move wins
        result = self.checkIfWin()
        if result != " ":
            self.win(result)
            return

    def createButtons(self, f): #function that creates the buttons
        buttons = []
        for i in range(3):
            for j in range(3): #https://www.delftstack.com/howto/python-tkinter/how-to-change-the-tkinter-button-size/
                btn = Button(f, text=str(self.boardData[i*3+j]), image=self.pixelSize, width=100, height=100, compound="bottom",
                                command=partial(self.onClick, i*3+j), font=self.buttonFont) #https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop
                btn.grid(column=j+1, row=i+1)
                buttons.append(btn)
        return buttons

    def getEmpty(self, board): #accessory function to get indices of empty cells
        return [i for i in range(len(board)) if board[i] == " "]

    def randomAgent(self, turn, curBoard): #random agent for testing gui
        possibleMoves = self.getEmpty(curBoard)
        return random.choice(possibleMoves)

    def minMaxGameOver(self, board): #checks if state is finished
        for i in range(3): #checks horizontally
            if len(set(board[i*3:i*3+3])) == 1 and board[i*3] != " ":
                return board[i*3]

        for i in range(3): #checks vertically
            if len(set(board[i::3])) == 1 and board[i] != " ":
                return board[i]

        if(len(set(board[::4]))==1 and board[0] != " "): #checks diagonally left
            return board[0]

        if(len(set(board[2:-2:2]))==1 and board[2] != " "): #checks diagonally right
            return board[2]

        if len([i for i in board if i == " "]) == 0: #Checks if draw
            return "D"
        return " "

    def minMaxAgent(self, aiFlag, Board): #main minmax agent
        possibleMoves = self.getEmpty(Board) #gets empty cells

        print("AiFlag:", aiFlag) #print statements for debugging
        print("Board:", Board)
        print("PosMoves", possibleMoves)

        if aiFlag: #max
            bestMove = {"cell": -1, "score": NEG_INF}
        else: #min
            bestMove = {"cell": -1, "score": POS_INF}

        evaluation = self.minMaxGameOver(Board) #checks if state is end state
        if evaluation != " ":
            if evaluation == self.aiTurn: #base case for ai's win
                return {"cell": -1, "score": 1}
            elif evaluation == self.turn: #base case for player win
                return {"cell": -1, "score": -1}
            elif evaluation == "D": #base case if draw
                return {"cell": -1, "score": 0}

        for move in possibleMoves: #iterates through all possible empty cells
            curBoard = Board[:] #makes a copy of the board
            curBoard[move] = self.aiTurn if aiFlag else self.turn #makes the move depending on max or min
            result = self.minMaxAgent(not aiFlag, curBoard) #recursive statement that changes min to max and vice versa
            curBoard[move] = " "
            result["cell"] = move

            if aiFlag: #case if max
                if result["score"] > bestMove["score"]:
                    bestMove = result #changes best move
            else: #case if min
                if result["score"] < bestMove["score"]:
                    bestMove = result #changes best move

        return bestMove

class PopUp(Tk): #class for pop up 
    def __init__(self):
        global playerChoice

        super(PopUp, self).__init__()
        self.minsize(200,50)
        self.resizable(0,0)
        playerChoice = "exit"

        self.title("Choose an option")

        self.frame = Frame(self)
        self.frame.grid(column=0, row=0, sticky=(N,W,E,S))

        # self.titleLabel = Label(self.frame, text="Choose an option:\n")
        # self.titleLabel.grid(column=1, row=1)

        self.xButton = Button(text="X", command=self.setX)
        self.xButton.grid(column=2, row=1)

        self.oButton = Button(text="O", command=self.setO)
        self.oButton.grid(column=3, row=1)

        self.exitButton = Button(text="Exit", command=self.destroy)
        self.exitButton.grid(column=4, row=1)

    def setO(self): #sets player turn to O
        global playerChoice
        playerChoice = "O"
        self.destroy()

    def setX(self): #sets player turn to X
        global playerChoice
        playerChoice = "X"
        self.destroy()

popup = PopUp()
popup.mainloop()

if playerChoice != "exit":
    root = TicTacToe()
    root.mainloop()
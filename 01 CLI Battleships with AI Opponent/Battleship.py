import random
import time

#Function to print the board
def printBoard(playerBoard, aiBoard):
    print(" ╔ Your Board                     | ╔ Enemy's Board")
    print(" ║ 1 ╦ 2 ╦ 3 ╦ 4 ╦ 5 ╦ 6 ╦ 7 ╦ 8 ╗| ║ 1 ╦ 2 ╦ 3 ╦ 4 ╦ 5 ╦ 6 ╦ 7 ╦ 8 ╗")
    print(" ╠═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗", end="")
    print("|",end="")
    print(" ╠═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗")
    for x in range(8):
        line = ""
        line = line + str(x+1)
        for y in range(8):
            line = line + "║"
            if playerBoard[x][y] == "~":
                line = line + "~~~"
            elif playerBoard[x][y] == "X":
                line = line + " X "
            elif playerBoard[x][y] == "O":
                line = line + " O "
            elif playerBoard[x][y] == "!":
                line = line + " ! "
            elif playerBoard[x][y] == "F":
                line = line + " F "
        line = line + "║"
        line = line + "|"
        line = line + str(x+1)
        for z in range(8):
            line = line + "║"
            if aiBoard[x][z] == "~":
                line = line + "~~~"
            elif aiBoard[x][z] == "X":
                line = line + " X "
            elif aiBoard[x][z] == "O":
                line = line + "~~~"
            elif aiBoard[x][z] == "!":
                line = line + " ! "
            elif aiBoard[x][z] == "F":
                line = line + " F "
        line = line + ("║")
        print(line)
        if x < 7:
            print(" ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣| ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣")
        else:
            print(" ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝| ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝")

# Used to check if tile is water (For ship placement logic)
def IsWater(tile):
    if tile == "~":
        return True
    else:
        return False

def PlaceShip(PlayerBoard, AiBoard):
    #Tuple for sizes of ships to be placed
    Ships = [2,3,3,4,5]
    ShipList = []
    print("═══════════════════════════════════════════════")
    printBoard(PlayerBoard, AiBoard)
    print("This system places ships left to right or top to bottom")
    #Loop for placing all the ships
    for ship in Ships:
        ShipCoords = []
        placing = True
        
        while placing:
            placing = False
            print("Placing ship with length: ", ship)
            #Inputs with input validation for orientation, row and column
            while True:
                orientation = input("Choose an orientation Admiral ('h' for horizontal and 'v' for vertical): ")
                if orientation not in ("h", "v"):
                    print("Please input 'h' for horizontal and 'v' for vertical")
                else:
                    break
                
            while True:
                try:
                    row = int(input("Choose a row to place in Admiral: ")) - 1
                except ValueError:
                    print("Please input an integer between and 1-8 Admiral")
                    continue
                else:
                    if row > 7 or row <= 0:
                        print("Please input an integer between and 1-8")
                        continue
                    else:
                        break
            while True:
                try:
                    col = int(input("Choose a column to place in Admiral: ")) - 1
                except ValueError:
                    print("Please input an integer between and 1-8 Admiral")
                    continue
                else:
                    if col > 7 or col <= 0:
                        print("Please input an integer between and 1-8")
                        continue
                    else:
                        break
            #For placing horizontal ships
            if orientation == "h":
                if (col + ship) > 8:
                    placing = True
                    print("You cannot place a ship there Admiral")
                    continue
                #Validating that ship is placeable by putting all coords into a list and confirming they are all empty spaces
                else:
                    elements = []
                    for length in range(ship):  
                        elements.append(PlayerBoard[row][col+length])
                    
                    for cells in elements:
                        if not IsWater(cells):
                            placing = True
                            print("You cannot place a ship there Admiral")
                            break
                        else:
                            continue
                    #Placing the ships and saving their coordinates to a list
                    else:
                        for length in range(ship):
                            PlayerBoard[row][col+length] = "O"
                            coord = str(row) + str(col+length)
                            ShipCoords.append(coord)
            #For placing vertical ships
            elif orientation == "v":
                if (row + ship) > 8:
                    placing = True
                    print("You cannot place a ship there Admiral")
                    continue
                else:
                    elements = []
                    for length in range(ship):
                        elements.append(PlayerBoard[row+length][col])
                    
                    for cells in elements:
                        if not IsWater(cells):
                            placing = True
                            print("Cannot Place! Try again")
                            break
                        else:
                            continue
                        
                    else:
                        for length in range(ship):
                            PlayerBoard[row+length][col] = "O"
                            coord = str(row+length) + str(col)
                            ShipCoords.append(coord)
            printBoard(PlayerBoard, AiBoard)
        ShipList.append(ShipCoords)
    return ShipList, Ships

#Same as PlaceShip but random coordinates and orientations
def RandomShipPlace(board):
#Tuple for sizes of ships to be placed
    Ships = [2,3,3,4,5]
    HV = ("h","v")
    ShipList = []
    #Loop for placing all the ships
    for ship in Ships:
        ShipCoords = []
        placing = True
        while placing:
            orientation = HV[random.randint(0,1)]
            row = random.randint(0,7)
            col = random.randint(0,7)
            #For horizontal ships
            if orientation == "h":
                if (col + ship) > 8:
                    placing = True
                    continue
                else:
                    elements = []
                    for length in range(ship):  
                        elements.append(board[row][col+length])
                    for cells in elements:
                        if not IsWater(cells):
                            placing = True
                            break
                        else:
                            continue

                    else:
                        for length in range(ship):
                            
                            if (row != 0) and board[row-1][col+length] == "~":
                                board[row-1][col+length] = "P"
                            elif (row != 7) and board[row+1][col+length] == "~":
                                board[row+1][col+length] = "P"

                            board[row][col+length] = "O"
                            
                            coord = str(row) + str(col+length)
                            ShipCoords.append(coord)
                        placing = False
                        
            #For vertical ships
            elif orientation == "v":
                if (row + ship) > 8:
                    placing = True
                    continue
                else:
                    elements = []
                    for length in range(ship):
                        elements.append(board[row+length][col])
                    for cells in elements:
                        if not IsWater(cells):
                            placing = True
                            break
                        else:
                            continue
                    else:
                        for length in range(ship):
                            
                            if (col != 0) and board[row+length][col-1] == "~":
                                board[row+length][col-1] = "P"
                            elif (col != 7)and board[row+length][col+1] == "~":
                                board[row+length][col+1] = "P"

                            board[row+length][col] = "O"
                            coord = str(row+length) + str(col)
                            ShipCoords.append(coord)
                        placing = False

        ShipList.append(ShipCoords)
        
    r = 0
    c = 0
    for line in board:
        c = 0
        for x in line:
            if board[r][c] == "P":
                board[r][c] = "~"
            c = c + 1
        r = r + 1
                
    return ShipList, Ships


def GameLoop(Load):
    #Initialization of Variables
    #Initialize Boards
    PlayerBoard = [["~" for x in range(8)] for x in range(8)]
    AiBoard = [["~" for x in range(8)] for x in range(8)]
    #Places Ships
    if not Load:
        print("═══════════════════════════════════════════════")
        print("Would you like to place ships manually or have them placed randomly?")
        print("[1] Manual")
        print("[2] Random")
        
        while True:
            try:
                placement = int(input("Choose an option: "))
            except ValueError:
                print("That's not an option")
                continue
            else:
                if placement > 2 or placement <= 0:
                    print("That's not an option")
                    continue
                else:
                    break
        
        if placement == 1:
            PlayerShipCoords, PlayerShipHealths = PlaceShip(PlayerBoard, AiBoard)
        elif placement == 2:
            PlayerShipCoords, PlayerShipHealths = RandomShipPlace(PlayerBoard)

        AiShipCoords, AiShipHealths = RandomShipPlace(AiBoard)
    
    #Base Healths
    PlayerMoves = 0
    PlayerHealth = 17
    AiHealth = 17
    AiVariables = {"PreviousRow": 0, "PreviousCol": 0, "HitShip": False, "ShipEnds": 2, "ShipOrientation":"", "HitSide":"", "ToHit": [], "CheckedSides": [], "SweepCounter": 1, "Collateral": [], "LastHit": "" , "RowHit": 0, "ColHit": 0, "SinkShip": False}

    #Code block for loading games
    if Load:
        PlayerBoard, AiBoard, PlayerShipCoords, PlayerShipHealths, AiShipCoords, AiShipHealths, PlayerMoves, PlayerHealth, AiHealth, AiVariables = LoadGame()
        print("Game Loaded!")
    print("═══════════════════════════════════════════════")
    printBoard(PlayerBoard, AiBoard)
    print("Lets do this Admiral! We're counting on you")
    print("Score: ", PlayerMoves,"(The lower the better)")
    print("Player Ships Remaining: ", PlayerHealth)
    print("Enemy Ships Remaining: ", AiHealth)
    #Main Game Loop
    inGame = True
    while inGame:
        decision = GameMenu()

        if decision == 1 or decision == 2:
            if decision == 1:
                row, col = PlayerMove(AiBoard)
            if decision == 2:
                row, col = RandomPlayerMove(AiBoard)

            time.sleep(0.5)
            
            PlayerMoves = PlayerMoves + 1
            AiRow, AiCol = AiAttack(AiVariables, PlayerBoard)
            PlayerHealth, AiHealth = Battle(row, col, AiRow, AiCol, AiVariables, PlayerBoard, AiBoard, PlayerHealth, AiHealth, PlayerShipHealths, AiShipHealths, PlayerShipCoords, AiShipCoords)
            SinkCheck(PlayerShipCoords, AiShipCoords, PlayerShipHealths, AiShipHealths, PlayerBoard, AiBoard, AiVariables)
            time.sleep(0.5)
            print("═══════════════════════════════════════════════")
            printBoard(PlayerBoard, AiBoard)
            time.sleep(0.5)
            print("Score: ", PlayerMoves)
            print("Player Ships Remaining: ", PlayerHealth)
            print("Enemy Ships Remaining: ", AiHealth)
            #AiVariableCheck(AiVariables)

            if AiHealth == 0:
                print("We did it Admiral! Splendid Work!")
                inGame = False
                SaveHighScores(PlayerMoves)
                LoadHighScores()
                break
            
            elif PlayerHealth == 0:
                inGame = False
                print("We'll get them next time")
                LoadHighScores()
                break
        
        elif decision == 3:
            SaveGame(PlayerBoard, AiBoard, PlayerShipCoords, PlayerShipHealths, AiShipCoords, AiShipHealths, PlayerMoves, PlayerHealth, AiHealth, AiVariables)
            print("Game has been saved!")
            printBoard(PlayerBoard, AiBoard)
            print("Score: ", PlayerMoves)
            print("Player Ships Remaining: ", PlayerHealth)
            print("Enemy Ships Remaining: ", AiHealth)

        elif decision == 4:
            SaveGame(PlayerBoard, AiBoard, PlayerShipCoords, PlayerShipHealths, AiShipCoords, AiShipHealths, PlayerMoves, PlayerHealth, AiHealth, AiVariables)
            print("Game has been saved!")
            break

        elif decision == 5:
            break
        
        time.sleep(0.5)

def PlayerMove(AiBoard):
    print("Pinpoint the coordinates Admiral")
    time.sleep(0.5)
    Attacking = True
    while Attacking:
        Attacking = False

        #Input with validation for row
        while True:
            try:
                row = int(input("Row: ")) - 1
            except ValueError:
                print("Please input an integer between and 1-8 Admiral")
                continue
            else:
                if row > 7 or row < 0:
                    print("Please input an integer between and 1-8 Admiral")
                    continue
                else:
                    break

        #Input with Validation for column
        while True:
            try:
                col = int(input("Col: ")) - 1
            except ValueError:
                print("Please input an integer between and 1-8")
                continue
            else:
                if col > 7 or col < 0:
                    print("Please input an integer between and 1-8 Admiral")
                    continue
                else:
                    break

        #Check if coordinate has been shot
        if not ValidMove(AiBoard[row][col]):
            print("Coordinate already shot! Choose another")
            Attacking = True
        else:
            return row, col

def RandomPlayerMove(AiBoard):
    #input("Enter to randomly shoot")
    print("We're attacking the Enemy Admiral!")
    time.sleep(0.5)
    row = random.randint(0,7)
    col = random.randint(0,7)

    while not ValidMove(AiBoard[row][col]):
        row = random.randint(0,7)
        col = random.randint(0,7)
    print("We're attacking Row: ", row+1, " Col: ", col+1)
    return row, col

def Battle(row, col, AiRow, AiCol, AiVariables, PlayerBoard, AiBoard, PlayerHealth, AiHealth, PlayerShipHealths, AiShipHealths, PlayerShipCoords, AiShipCoords):
    time.sleep(0.5)
    #Player Attacks
    if AiBoard[row][col] == "~":
        AiBoard[row][col] = "X"
        print("We missed Admiral! Try Again")
        
    elif AiBoard[row][col] == "O":
        AiBoard[row][col] = "!"
        AiHealth = AiHealth - 1
        x = ConvertToCoord(row,col)
        AttackShip(AiShipHealths, x, AiShipCoords)
        print("We got em Admiral! Keep it up!")
    time.sleep(0.5)
    #Ai Attacks
    if PlayerBoard[AiRow][AiCol] == "~":
        PlayerBoard[AiRow][AiCol] = "X"
        LastHit = "X"
        print("They missed our ships!")
        
    elif PlayerBoard[AiRow][AiCol] == "O":
        PlayerBoard[AiRow][AiCol] = "!"
        LastHit = "!"
        PlayerHealth = PlayerHealth - 1
        AiVariables["Collateral"].append(ConvertToCoord(AiRow, AiCol))
        y = ConvertToCoord(AiRow, AiCol)
        AttackShip(PlayerShipHealths, y, PlayerShipCoords)
        AiSinkCheck(PlayerShipCoords, PlayerShipHealths, AiRow, AiCol, AiVariables)
        print("They hit one of our ships admiral!")

    AiVariables["PreviousRow"], AiVariables["PreviousCol"], AiVariables["LastHit"] = AiRow, AiCol, LastHit

    return PlayerHealth, AiHealth

def ValidMove(tile):
    if tile == "~" or tile == "O":
        return True
    if tile == "X" or tile == "!" or tile == "F":
        return False

# Smart Ai Opponent
def AiAttack(AiVariables, PlayerBoard):
    # Checks if there are unsunken ships
    if not AiVariables["HitShip"] and (len(AiVariables["Collateral"]) != 0):
        AiVariables["HitShip"] = True
        RandomCoord = random.choice(AiVariables["Collateral"])
        AiVariables["Collateral"].remove(RandomCoord)
        AiVariables["RowHit"] = int(RandomCoord[0])
        AiVariables["ColHit"] = int(RandomCoord[1])
        AiVariables["ShipOrientation"] = ""
        AiVariables["HitSide"] = ""
        DirectionAdder(AiVariables["RowHit"], AiVariables["ColHit"], AiVariables)

    # Decision Making for Ai
    reset = True
    while reset:
        reset = False
        if not AiVariables["HitShip"]:
            row, col = RandomCheckerBoard(AiVariables, PlayerBoard)
        else:
            if AiVariables["ShipOrientation"] == "":
                row, col, reset = OrientationFinder(AiVariables, PlayerBoard)
            else:
                row, col, reset = Sweeper(AiVariables, PlayerBoard)
                ResetSweep(AiVariables)


    return row, col

# Attacks a random empty spot on the Board
def RandomAttack(AiVariables, PlayerBoard):
    #print("Ai is Randomly Attacking")
    AiRow = random.randint(0,7)
    AiCol = random.randint(0,7)
    
    while not ValidMove(PlayerBoard[AiRow][AiCol]):
        AiRow = random.randint(0,7)
        AiCol = random.randint(0,7)

    if PlayerBoard[AiRow][AiCol] == "O":
        print("Ai has found a ship!")
        AiVariables["HitShip"] = True
        AiVariables["SinkShip"] = False
        AiVariables["RowHit"] = AiRow
        AiVariables["ColHit"] = AiCol
        DirectionAdder(AiRow, AiCol, AiVariables)
    
    return AiRow, AiCol

# Attacks the Board in a checkerboard pattern
def RandomCheckerBoard(AiVariables, PlayerBoard):
    #print("Ai is CheckerBoarding")
    AiRow = random.randint(0,7)
    AiCol = random.randint(0,7)

    counter = 0

    while not ((((AiRow % 2 == 0) and (AiCol % 2 == 1)) or ((AiRow % 2 == 1) and (AiCol % 2 == 0))) and ValidMove(PlayerBoard[AiRow][AiCol])):
        AiRow = random.randint(0,7)
        AiCol = random.randint(0,7)
        counter = counter + 1

        if counter == 32: #Done if the checkerboard is exhausted
            AiRow, AiCol = RandomAttack(AiVariables, PlayerBoard)
            return AiRow, AiCol

    if PlayerBoard[AiRow][AiCol] == "O":
        #print("Ai has found a ship!")
        AiVariables["HitShip"] = True
        AiVariables["SinkShip"] = False
        AiVariables["RowHit"] = AiRow
        AiVariables["ColHit"] = AiCol
        DirectionAdder(AiRow, AiCol, AiVariables)

    return AiRow, AiCol

# Preparation for Finding the orientation of a hit ship
def DirectionAdder(AiRow, AiCol, AiVariables):
    #When ship is on corners/upper and lower edges
    if AiRow == 0:
        AiVariables["ToHit"].append("d")
        if AiCol == 0:
            AiVariables["ToHit"].append("r")
        elif AiCol == 7:
            AiVariables["ToHit"].append("l")
        else:
            AiVariables["ToHit"].extend(["r", "l"])
    elif AiRow == 7:
        AiVariables["ToHit"].append("u")
        if AiCol == 0:
            AiVariables["ToHit"].append("r")
        elif AiCol == 7:
            AiVariables["ToHit"].append("l")
        else:
            AiVariables["ToHit"].extend(["r", "l"])

    #When ships are on the side edges
    elif AiCol == 0:
        AiVariables["ToHit"].extend(["r","u","d"])
    elif AiCol == 7:
        AiVariables["ToHit"].extend(["l","u","d"])

    #When ships are in the middle of board
    else:
        AiVariables["ToHit"].extend(["r","l","u","d"])

#Find the orientation of ship hit
def OrientationFinder(AiVariables, PlayerBoard):
    #print("Ai is Finding Ship Orientation")
    Finding = True
    while Finding:
        Finding = False

        if len(AiVariables["ToHit"]) == 0:
            AiVariables["ShipEnds"] = 0
            ResetSweep(AiVariables)
            return 0, 0, True
        #Randomizer to choose side to hit
        choice = random.choice(AiVariables["ToHit"])
        AiVariables["CheckedSides"].append(choice)
        AiVariables["ToHit"].remove(choice)
        
        if choice == "u":
            AiRow = AiVariables["RowHit"] - 1
            AiCol = AiVariables["ColHit"]
        elif choice == "d":
            AiRow = AiVariables["RowHit"] + 1
            AiCol = AiVariables["ColHit"]
        elif choice == "l":
            AiRow = AiVariables["RowHit"]
            AiCol = AiVariables["ColHit"] - 1
        elif choice == "r":
            AiRow = AiVariables["RowHit"]
            AiCol = AiVariables["ColHit"] + 1

        #Checks if coordinates have already been hit, if hit then restarts loop to move on onto the next
        if not ValidMove(PlayerBoard[AiRow][AiCol]):
            Finding = True
            continue

        if PlayerBoard[AiRow][AiCol] == "O":
            AiVariables["HitSide"] = choice
            #print("choice:" + choice)
            AiVariables["CheckedSides"].remove(choice)
            
            if choice == "u" or choice == "d":
                AiVariables["ShipOrientation"] = "v"
                if ((choice == "u") and ("d" in AiVariables["CheckedSides"])) or ((choice == "d") and ("u" in AiVariables["CheckedSides"])):
                    AiVariables["ShipEnds"] = AiVariables["ShipEnds"] - 1
                    
            elif choice == "l" or choice == "r":
                AiVariables["ShipOrientation"] = "h"
                if ((choice == "r") and ("l" in AiVariables["CheckedSides"])) or ((choice == "l") and ("r" in AiVariables["CheckedSides"])):
                    AiVariables["ShipEnds"] = AiVariables["ShipEnds"] - 1

            #Resets Variables
            AiVariables["ToHit"] = []
            AiVariables["CheckedSides"] = []
            AiVariables["HitSide"] = choice
            choice = ""
    
    return AiRow, AiCol, False

# "Sweeps" for the remaining parts of a found ship
def Sweeper(AiVariables, PlayerBoard):
    #print("Ai is Sweeping out Ship")
    Sweeping = True
    while Sweeping:
        Sweeping = False
    
        if AiVariables["ShipOrientation"] == "h":
            LastCoord = AiVariables["PreviousCol"]
            
        elif AiVariables["ShipOrientation"] == "v":
            LastCoord = AiVariables["PreviousRow"]

        # Takes note of where to hit next
        AiVariables["SweepCounter"] = AiVariables["SweepCounter"] + 1

        # Restart loop if last hit is edge
        if (LastCoord <= 0 or LastCoord >= 7) and (AiVariables["LastHit"] == "!"):
            ResetSweep(AiVariables)
            if AiVariables["LastHit"] == "!":
                #print("Reversal: Edge reverse")
                ReverseDirection(AiVariables)
                if AiVariables["ShipEnds"] == 0:
                    ResetSweep(AiVariables)
                    return AiVariables["RowHit"], AiVariables["ColHit"], True
                Sweeping = True
                continue
            

        #If Last target is not part of edges
        elif (LastCoord > 0 and LastCoord < 7) or (AiVariables["LastHit"] == "X"):
            
            #Coordinate adjuster based on last hit using sweepcounter
            if AiVariables["HitSide"] == "l":
                AiRow = AiVariables["RowHit"]
                AiCol = AiVariables["ColHit"] - AiVariables["SweepCounter"]
            elif AiVariables["HitSide"] == "r":
                AiRow = AiVariables["RowHit"]
                AiCol = AiVariables["ColHit"] + AiVariables["SweepCounter"]
            if AiVariables["HitSide"] == "u":
                AiRow = AiVariables["RowHit"] - AiVariables["SweepCounter"]
                AiCol = AiVariables["ColHit"]
            elif AiVariables["HitSide"] == "d":
                AiRow = AiVariables["RowHit"] + AiVariables["SweepCounter"]
                AiCol = AiVariables["ColHit"]

            
            if AiRow > 7 or AiRow < 0 or AiCol > 7 or AiCol < 0:
                AiVariables["ShipEnds"] = 0
                ResetSweep(AiVariables)
                return AiVariables["RowHit"], AiVariables["ColHit"], True

            #Checks if Next Square is possible to hit or not
            if not ValidMove(PlayerBoard[AiRow][AiCol]):
                #print("Reversal: Unhittable reverse")
                ReverseDirection(AiVariables)
                return AiVariables["RowHit"], AiVariables["ColHit"], True

            elif PlayerBoard[AiRow][AiCol] == "~":
                #print("Reversal: Ocean reverse")
                ReverseDirection(AiVariables)
                return AiRow, AiCol, False
            
            else:
                #print("Reversal: No Reversal")
                return AiRow, AiCol, False
            
        # Contingency code if ai bugs out        
        else:
            #print("Sweeper Failed")
            AiVariables["ShipEnds"] = 0
            return AiVariables["RowHit"], AiVariables["ColHit"], True

# Reverses the direction in the Sweeper function
def ReverseDirection(AiVariables):
    #print("Ai has reversed sweep")
    AiVariables["SweepCounter"] = 0
    AiVariables["ShipEnds"] = AiVariables["ShipEnds"] - 1
    AiVariables["PreviousRow"] = AiVariables["RowHit"]
    AiVariables["PreviousCol"] = AiVariables["ColHit"]
    if AiVariables["ShipOrientation"] == "h":
        if AiVariables["HitSide"] == "l":
            AiVariables["HitSide"] = "r"
        else:
            AiVariables["HitSide"] = "l"
    elif AiVariables["ShipOrientation"] == "v":
        if AiVariables["HitSide"] == "u":
            AiVariables["HitSide"] = "d"
        else:
            AiVariables["HitSide"] = "u"

# Resets the Sweeper function
def ResetSweep(AiVariables):
    if AiVariables["ShipEnds"] <= 0:
        AiVariables["HitShip"] = False
        AiVariables["SinkShip"] = False
        AiVariables["SweepCounter"] = 1
        AiVariables["ShipOrientation"] = ""
        AiVariables["LastHit"] = ""
        AiVariables["HitSide"] = ""
        AiVariables["ShipEnds"] = 2

#Debugging tool for keeping track of Ai behavior
def AiVariableCheck(AiVariables):
    for key, value in AiVariables.items():
        print(key, ": ", value)

# counts remaining ships (Debugging tool)
def count(board):
    total = 0
    for line in board:
        for cell in line:
            if cell == "~" or cell == "O":
                total = total + 1
    return total

# Converts inputs to coordinate data
def ConvertToCoord(row, col):
    coord = str(row) + str(col)
    return coord

# Sinks the ship if all parts have been hit
def SinkShip(Ship, ShipList, Board):
    TempRow = -1
    TempCol = -1
    
    for row in Board:
        TempCol = -1
        TempRow = TempRow + 1
        for col in row:
            TempCol = TempCol + 1
            TempCoord = ConvertToCoord(TempRow,TempCol)
            if TempCoord in ShipList[Ship]:
                Board[TempRow][TempCol] = "F"

# Checks for Sunk Ships
def SinkCheck(PlayerShipCoords, AiShipCoords, PlayerShipHealths, AiShipHealths, PlayerBoard, AiBoard, AiVariables):
    counterx = -1
    for x in PlayerShipHealths:
        counterx = counterx + 1
        if x == 0:
            SinkShip(counterx, PlayerShipCoords, PlayerBoard)
            print("One of our ships has been sunk Admiral!")
            PlayerShipHealths[counterx] = 99

    countery = -1
    for y in AiShipHealths:
        countery = countery + 1
        if y == 0:
            SinkShip(countery, AiShipCoords, AiBoard)
            print("Booyah! We sunk one of the ships Admiral!")
            AiShipHealths[countery] = 99


# Function for checking if the ai has sunk a ship
def AiSinkCheck(PlayerShipCoords, PlayerShipHealths, AiRow, AiCol, AiVariables):
    Ship = IdentifyShip(ConvertToCoord(AiRow,AiCol), PlayerShipCoords)
    if PlayerShipHealths[Ship] == 0:
        AiVariables["ShipEnds"] = 0
        ResetSweep(AiVariables)
        for x in PlayerShipCoords[Ship]:
            if x in AiVariables["Collateral"]:
                AiVariables["Collateral"].remove(x)

# Reduces the health of a ship when it is hit
def AttackShip(ShipHealths, Coord, ShipList):
    Ship = IdentifyShip(Coord, ShipList)
    ShipHealths[Ship] = ShipHealths[Ship] - 1

# Identifies a hit ship
def IdentifyShip(coord, ShipList):
    for ship in ShipList:
        for ShipCoords in ship:
            if coord == ShipCoords:
                ShipNumber = ShipList.index(ship)
                return ShipNumber

#Saves current game state to a file
def SaveGame(PlayerBoard, AiBoard, PlayerShipCoords, PlayerShipHealths, AiShipCoords, AiShipHealths, PlayerMoves, PlayerHealth, AiHealth, AiVariables):
    print("Choose a save slot")
    print("[1] Save Slot 1")
    print("[2] Save Slot 2")
    print("[3] Save Slot 3")
    print("[4] Custom Slot")

    while True:
        try:
            slot = int(input("Choose a slot: "))
        except ValueError:
            print("That's not a save slot")
            continue
        else:
            if slot > 4 or slot <= 0:
                print("That's not a save slot")
                continue
            else:
                break

    if slot == 1:
        savefile = open("SaveSlot1.txt", "w")
    if slot == 2:
        savefile = open("SaveSlot2.txt", "w")
    if slot == 3:
        savefile = open("SaveSlot3.txt", "w")
    if slot == 4:
        savename = input("Enter File Name: ")
        savefile = open(savename, "w")

    for line in PlayerBoard:
        for cell in line:
            savefile.write(cell)
            savefile.write(",")
        savefile.write("\n")
    savefile.write("\n")

    
    for line in AiBoard:
        for cell in line:
            savefile.write(cell)
            savefile.write(",")
        savefile.write("\n")
    savefile.write("\n")

    for ships in PlayerShipCoords:
        for x in ships:
            savefile.write(x)
            savefile.write(",")
        savefile.write("\n")
    savefile.write("\n")

    for ships in AiShipCoords:
        for x in ships:
            savefile.write(x)
            savefile.write(",")
        savefile.write("\n")
    savefile.write("\n")

    for health in PlayerShipHealths:
        savefile.write(str(health))
        savefile.write(",")
    savefile.write("\n")

    for health in AiShipHealths:
        savefile.write(str(health))
        savefile.write(",")
    savefile.write("\n")

    savefile.write(str(PlayerMoves))
    savefile.write("\n")
    savefile.write(str(PlayerHealth))
    savefile.write("\n")
    savefile.write(str(AiHealth))
    savefile.write("\n")

    for key, value in AiVariables.items():
        savefile.write(key)
        savefile.write("<#>")
        savefile.write(str(value))
        savefile.write("\n")
    
    savefile.close()

#Loads a game from a save file
def LoadGame():
    print("Choose a save slot")
    print("[1] Save Slot 1")
    print("[2] Save Slot 2")
    print("[3] Save Slot 3")
    print("[4] Custom Slot")

    while True:
        try:
            slot = int(input("Choose a slot: "))
        except ValueError:
            print("That's not a save slot")
            continue
        else:
            if slot > 4 or slot <= 0:
                print("That's not a save slot")
                continue
            else:
                break

    if slot == 1:
        savefile = open("SaveSlot1.txt", "r")
    if slot == 2:
        savefile = open("SaveSlot2.txt", "r")
    if slot == 3:
        savefile = open("SaveSlot3.txt", "r")
    if slot == 4:
        while True:
            try:
                savefile = open(input("Enter File Name: "))
            except FileNotFoundError:
                print("That's not a save slot, please input again")
                continue
            else:
                break
        
    masterlist = savefile.readlines()

    masterlist = [x[:-1] for x in masterlist]

    PlayerBoard = masterlist[0:8]
    AiBoard = masterlist[9:17]

    PlayerBoard = [x.split(",") for x in PlayerBoard]
    AiBoard = [x.split(",") for x in AiBoard]

    PlayerBoard = [x[:-1] for x in PlayerBoard]
    AiBoard = [x[:-1] for x in AiBoard]

    PlayerShipCoords = masterlist[18:23]
    AiShipCoords = masterlist[24:29]
    
    PlayerShipCoords = [x.split(",") for x in PlayerShipCoords]
    AiShipCoords = [x.split(",") for x in AiShipCoords]

    PlayerShipCoords = [x[:-1] for x in PlayerShipCoords]
    AiShipCoords = [x[:-1] for x in AiShipCoords]

    PlayerShipHealths = (masterlist[30]).split(",")
    AiShipHealths = (masterlist[31]).split(",")

    PlayerShipHealths = PlayerShipHealths[:-1]
    AiShipHealths = AiShipHealths[:-1]

    PlayerShipHealths = [int(x) for x in PlayerShipHealths]
    AiShipHealths = [int(x) for x in AiShipHealths]

    PlayerMoves = masterlist[32]
    PlayerHealth = masterlist[33]
    AiHealth = masterlist[34]

    PlayerMoves = int(PlayerMoves)
    PlayerHealth = int(PlayerHealth)
    AiHealth = int(AiHealth)

    AiVariables = {}
    Temp = masterlist[35:]

    Temp = [x.split("<#>") for x in Temp]

    for x in Temp:
        AiVariables[x[0]] = x[1]

    AiVariables["PreviousRow"] = int(AiVariables["PreviousRow"])
    AiVariables["PreviousCol"] = int(AiVariables["PreviousCol"])
    
    if AiVariables["HitShip"] == "False":
        AiVariables["HitShip"] = False

    elif AiVariables["HitShip"] == "True":
        AiVariables["HitShip"] = True
    
    AiVariables["ShipEnds"] = int(AiVariables["ShipEnds"])
    AiVariables["ToHit"] = (AiVariables["ToHit"]).strip('[]').split(', ')

    if AiVariables["ToHit"] == ['']:
        AiVariables["ToHit"] = []
    else:
        AiVariables["ToHit"] = [x[1:-1] for x in AiVariables["ToHit"]]

    AiVariables["CheckedSides"] = (AiVariables["CheckedSides"]).strip('[]').split(', ')

    if AiVariables["CheckedSides"] == ['']:
        AiVariables["CheckedSides"] = []
    else:
        AiVariables["CheckedSides"] = [x[1:-1] for x in AiVariables["CheckedSides"]]

    AiVariables["Collateral"] = (AiVariables["Collateral"]).strip('[]').split(', ')

    if AiVariables["Collateral"] == ['']:
        AiVariables["Collateral"] = []
    else:
        AiVariables["Collateral"] = [x[1:-1] for x in AiVariables["Collateral"]]

    AiVariables["SweepCounter"] = int(AiVariables["SweepCounter"])
    AiVariables["RowHit"] = int(AiVariables["RowHit"])
    AiVariables["ColHit"] = int(AiVariables["ColHit"])
    
    if AiVariables["SinkShip"] == "False":
        AiVariables["SinkShip"] = False

    elif AiVariables["SinkShip"] == "True":
        AiVariables["SinkShip"] = True
    
    return PlayerBoard, AiBoard, PlayerShipCoords, PlayerShipHealths, AiShipCoords, AiShipHealths, PlayerMoves, PlayerHealth, AiHealth, AiVariables

#Menu while in game
def GameMenu():
    print("═══════════════════════════════════════════════")
    print("[1] Attack the Enemy")
    print("[2] Attack Randomly")
    print("[3] Save Game")
    print("[4] Save and Exit")
    print("[5] Exit Without Saving")

    while True:
        try:
            selection = int(input("On your order Admiral: "))
        except ValueError:
            print("That's not something I can do Sir")
            continue
        else:
            if selection > 5 or selection <= 0:
                print("That's not something I can do Sir")
                continue
            else:
                break
    print("═══════════════════════════════════════════════")

    return selection

#Menu on startup
def MainMenu():
    while True:
        print("═══════════════════════════════════════════════")
        print("""
______       _   _   _           _     _        
| ___ \     | | | | | |         | |   (_)       
| |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __   
| ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \  
| |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) | 
\____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/  
                                        | |     
                                        |_|
By: Jarem Thimoty M. Arias
""")
        print("═══════════════════════════════════════════════")
        time.sleep(.75)
        print("""
[1] Play Game
[2] Load Game
[3] Check Hall of Fame
[4] Exit
    """)
        print("═══════════════════════════════════════════════")

        while True:
            try:
                selection = int(input("Select an Action Admiral: "))
            except ValueError:
                print("That's not something I can do Sir")
                continue
            else:
                if selection > 4 or selection <= 0:
                    print("That's not something I can do Sir")
                    continue
                else:
                    break

        if selection == 1:
            GameLoop(False)
        elif selection == 2:
            GameLoop(True)
        elif selection == 3:
            LoadHighScores()
        elif selection == 4:
            print("Thanks for playing Admiral!")
            break
        
        print("═══════════════════════════════════════════════")

#Saves the score at the end of a game to a file
def SaveHighScores(score):
    leaderboards = open("HighScores.txt", "a")
    while True:
        name = input("Please input a 4 letter name for the Hall of Fame: ")
        if len(name) > 4:
            print("Only 4 letters are allowed")
            continue
        else:
            break
        
    leaderboards.write(name)
    leaderboards.write("<#>")
    leaderboards.write(str(score))
    leaderboards.write("\n")
    leaderboards.close()

def getSecond(elem):
    return elem[1]

#Loads the high scores
def LoadHighScores():
    leaderboards = open("HighScores.txt", "r")
    
    print("Rank", end = "")
    print("\t", end = "")
    print("Name", end = "")
    print("\t", end = "")
    print("Score")
    print("═════════════════════")
    scores = []
    for line in leaderboards:
        tuple = ()
        temp = line.split("<#>")
        temp[1] = temp[1][:-1]
        temp[1] = int(temp[1])
        scores.append(temp)
        
    scores.sort(key=getSecond)

    rank = 1
    for x in scores:
        print(rank, end = "")
        print("\t", end = "")
        print(x[0], end = "")
        print("\t", end = "")
        print(x[1])
        rank = rank + 1
    print("═════════════════════")
    
    leaderboards.close()
    input("Press enter to go back to Main Menu")

MainMenu()


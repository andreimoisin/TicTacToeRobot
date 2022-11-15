# import webdriver
from email.policy import default
from pickle import TRUE
from telnetlib import GA
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


#create webdriver object
driver = webdriver.Chrome()

# get geeksforgeeks.org
driver.get("https://playtictactoe.org/")

# accept cookies politcis

try:
    driver.find_element(By.ID, 'consent').click()
except:
    print("No cookies!")

# close bottom add

sleep(1)

try:
    driver.find_element(By.ID, 'down').click()
except:
    print("No add to minimize!")

sleep(1)

# get element
RealBoard = driver.find_element(By.CLASS_NAME,'board')

restart = driver.find_element(By.CLASS_NAME, 'restart')

elementList = RealBoard.find_elements(By.CLASS_NAME, 'square')

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

myTurn = False
player = 1
computer = 2

def translateBoard(cls, imp):
    match cls:
        case "square top left":
            board[0][0] = imp
        case "square top":
            board[0][1] = imp
        case "square top right":
            board[0][2] = imp
        case "square left":
            board[1][0] = imp
        case "square":
            board[1][1] = imp
        case "square right":
            board[1][2] = imp
        case "square bottom left":
            board[2][0] = imp
        case "square bottom":
            board[2][1] = imp
        case "square bottom right":
            board[2][2] = imp

def updateBoard():

    print("Updating board...")
    print("")
    print("")
    print("")

    for box in elementList:
        #print(box.get_attribute("class"))
        try:
            box.find_element(By.CLASS_NAME, 'x')
            print("The cell is X! Class is: " + box.get_attribute("class"))
            translateBoard(box.get_attribute("class"), 1)
        except:
            #print("There is no x! Class is: " + box.get_attribute("class"))
            try:
                box.find_element(By.CLASS_NAME, 'o')
                print("The cell is 0! Class is: " + box.get_attribute("class"))
                translateBoard(box.get_attribute("class"), 2)
            except:
                print("The cell is EMPTY! Class is: " + box.get_attribute("class"))

    print("")
    print("Board is up-to-date!")
    print("")
    print("")
            
def clickBox(cls):
   print("Trying to click " + cls + "...")
   for box in elementList:
        if(box.get_attribute("class") == cls):
            box.click()
            print("Clicking " + cls)
            #print("Sleeping 2 seconds")
            print("")
            #sleep(2)


def getClass(i, j):
    match i, j:
        case 0, 0:
            return "square top left"
        case 0, 1:
            return "square top"
        case 0, 2:
            return "square top right"
        case 1, 0:
            return "square left"
        case 1, 1:
            return "square"
        case 1, 2:
            return "square right"
        case 2, 0:
            return "square bottom left"
        case 2, 1:
            return "square bottom"
        case 2, 2:
            return "square bottom right"


def isBoardEmpty(gameBoard):
    for i in range(3):
        for j in range(3):
            if gameBoard[i][j] != 0:
               return False
    print("The board is EMPTY!")
    return True

def isMovesLeft(gameBoard):
    for i in range(3):
        for j in range(3):
            if gameBoard[i][j] == 0:
               return True
    return False

def evaluateBoard(gameBoard):

    # check win on rows
    for x in range(3):
        if gameBoard[x][0] == gameBoard[x][1] and gameBoard[x][1] == gameBoard[x][2]:
            if gameBoard[x][0] == player:
                return 10
            if gameBoard[x][0] == computer:
                return -10

    # check win on columns
    for y in range(3):
        if gameBoard[0][y] == gameBoard[1][y] and gameBoard[1][y] == gameBoard[2][y]:
            if gameBoard[0][y] == player:
                return 10
            if gameBoard[0][y] == computer:
                return -10

    # check for diagonals
    if gameBoard[0][0] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[2][2]:
        if gameBoard[0][0] == player:
            return 10
        if gameBoard[0][0] == computer:
            return -10

    if gameBoard[0][2] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[2][0]:
        if gameBoard[0][2] == player:
            return 10
        if gameBoard[0][2] == computer:
            return -10

    #tie or game not finished yet
    return 0

def minimax(gameBoard, depth, myTurn) :
    score = evaluateBoard(gameBoard)
 
    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10) :
        return score
 
    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10) :
        return score
 
    # If there are no more moves and no winner then
    # it is a tie
    if isMovesLeft(gameBoard) == False:
        return 0
 
    # If this maximizer's move
    if myTurn :    
        best = -1000
 
        # Traverse all cells
        for i in range(3) :        
            for j in range(3) :
              
                # Check if cell is empty
                if (gameBoard[i][j]== 0) :
                 
                    # Make the move
                    gameBoard[i][j] = player
 
                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(gameBoard,
                                              depth + 1,
                                              not myTurn) - depth)
 
                    # Undo the move
                    gameBoard[i][j] = 0
        return best
 
    # If this minimizer's move
    else:
        best = 1000
 
        # Traverse all cells
        for i in range(3) :        
            for j in range(3) :
              
                # Check if cell is empty
                if (gameBoard[i][j] == 0) :
                 
                    # Make the move
                    gameBoard[i][j] = computer
 
                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not myTurn) - depth)
 
                    # Undo the move
                    gameBoard[i][j] = 0
        return best

def findBestMove(gameBoard) :
    bestVal = -1000
    bestMove = (-1, -1)
 
    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3) :    
        for j in range(3) :
         
            # Check if cell is empty
            if (gameBoard[i][j] == 0) :
             
                # Make the move
                gameBoard[i][j] = player
 
                # compute evaluation function for this
                # move.
                moveVal = minimax(gameBoard, 0, False)
 
                # Undo the move
                gameBoard[i][j] = 0
 
                # If the value of the current move is
                # more than the best value, then update
                # best/
                if (moveVal > bestVal) :               
                    bestMove = (i, j)
                    bestVal = moveVal
 
    print("The value of the best Move is :", bestVal)
    print()
    return bestMove

def playGame():

    for game in range(10):

        # Starting Game...
        # Checking if the board is empty to know who is moving next
        print("Starting game ", game)
        sleep(2)

        updateBoard()

        myTurn = isBoardEmpty(board)
            
        print(myTurn)

        for x in range(3):
            print(board[x])

        sleep(1)

        while isMovesLeft(board) and evaluateBoard(board) == 0:
            print("Calculating the next move...")
            move = findBestMove(board)

            clickBox(getClass(move[0], move[1]))
            sleep(2)
            updateBoard()

            for x in range(3):
                print(board[x])

        print("The game ", game, " is over!")
        sleep(3)
        #restart.click()

        
        
playGame()

# send keys
#element.click()

#creating the board game
# 1 --> X
# 2 --> 0
# 0 --> EMPTY


sleep(5)
#input()
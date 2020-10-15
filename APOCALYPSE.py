import turtle
import math
import time
import random
import copy


'''
Temporary "constants" until compiled into one program...
'''
NUM_OF_SQUARES = 25
WIN_SIZE_X = 450
WIN_SIZE_Y = 450
SIZE_PER_CELL = 60
CELLS_PER_DIMENSION = int(math.sqrt(NUM_OF_SQUARES))
WIDTH = SIZE_PER_CELL * CELLS_PER_DIMENSION
MARGIN_X = (WIN_SIZE_X - WIDTH)/2
MARGIN_Y = (WIN_SIZE_Y - WIDTH)/2
'''
...end of "constants"
'''
#-------------------------------------------------THIS PART MAKES THE GAMEBOARD AND UPLOADS THE PIECES---------------------------------------
#Assorted random constants
COLUMNS = "abcde" #Replaces previous array of the characters
notifier = turtle.Turtle()
notifier.ht()
notifier.up()
notifier.goto(0, -50)

# This function draws a welcoming messages, waits, and then clears the message before the game begins
# Parameters:
# 		t: (turtle.Turtle) Turtle for drawing the welcome message
# 		window: (turtle._Screen) The screen, which gets cleared at the end
# Returns:
# 		None
def drawWelcome(t, window):
        t.penup()
        t.left(180)
        t.forward(200)
        t.right(90)
        t.forward(0)
        t.color("green")
        t.write("Apocalypse", font = ("Times New Roman", 60))
        t.hideturtle()
        #delay
        time.sleep(2)
        window.clear()

# This function prepares the visuals for the "background" of the game, including drawing the game board and setting window size
# Parameters:
# 		window: (turtle._Screen) Window to modify the size of
# Returns:
# 		None  
def drawGameBoard(window):
        window.setup(WIN_SIZE_X, WIN_SIZE_Y)
        
        window.setworldcoordinates(-MARGIN_X, -MARGIN_Y, WIDTH + MARGIN_X, WIDTH + MARGIN_Y)
        window.tracer(2)
        border_turtle= turtle.Turtle()
        #Speeds up drawing
        border_turtle.hideturtle()
        border_turtle.speed(0)
        #Bright color is chosen. Dark squares will be drawn overtop an all-bright board.
        border_turtle.color("burlywood")
        border_turtle.begin_fill()
        border_turtle.goto(0, WIDTH)
        for i in range(4):
                border_turtle.forward(WIDTH)
                border_turtle.right(90)

        border_turtle.end_fill()
        square = turtle.Turtle()
        square.hideturtle()
        square.speed(0)
        #Dark color is chosen
        square.color("sienna")
        square.up()
        square.goto(0, WIDTH)
        for i in range(5):
                #Turtle starts at bottom-left of each row's left most square
                square.goto(0, WIDTH - SIZE_PER_CELL * i)
                #Determines if turtle begins drawing dark square at an edge, or at an indent, then moves the turtle
                square.forward((i % 2) * SIZE_PER_CELL)
                #First, determine how many dark squares are needed, then begin loop
                for j in range(3 - (i % 2)):
                        square.begin_fill()
                        #Draws the dark cell
                        for k in range(4):
                                square.forward(SIZE_PER_CELL)
                                square.right(90)

                        square.end_fill()
                        #Moves in position to draw new cell
                        square.forward(SIZE_PER_CELL * 2)
                                                                
        writer = turtle.Turtle()
        writer.speed(0)
        writer.hideturtle()
        writer.penup()
        #Turtle's default font size (8) works best with WIDTH of 125; sizes for other WIDTHs adjusted accordingly
        font_size = 8 * (WIDTH/125)
        #Positions turtle around top-left of board, to start writing the "letters" on top for each column
        writer.goto(SIZE_PER_CELL/2, WIDTH + SIZE_PER_CELL/2)
        
        for i in COLUMNS:
                writer.write(i, align="center", font = font_size)
                writer.forward(SIZE_PER_CELL)
        #Positions turtle around top-left of board; rotates to face down and then works downwards
        writer.goto(-SIZE_PER_CELL/2, WIDTH - SIZE_PER_CELL/2)
        writer.right(90)
        
        for i in range(1, 6):
                writer.write(i, align="center", font = font_size)
                writer.forward(SIZE_PER_CELL)   
                                        
#Function takes a square from the board and returns the pixel value of it's centre on that axis
# Parameters:
# 		x: (float) x value (from 0 to 4) of the starting square's relative position to other squares
# 		y: (float) y value (from 0 to 4) of the starting square's relative position to other squares
# Returns:
# 		coordinate_x, coordinate_y: (tuple) The coordinates, in pixels, of the square's centre
def coordinates(x, y):
        coordinate_x = SIZE_PER_CELL * (2 * x + 1)/2
        coordinate_y = WIDTH - (SIZE_PER_CELL * (2 * y + 1)/2)
        return (coordinate_x, coordinate_y)     
        
#----------------------------------------------------------THIS PART CHECKS FOR PIECES--------------------------------
# This function checks if a square is occupied by a white pawn
# Parameters:
# 		game_state: (list) the game_state
# 		column: (int) column number to check
# 		row: (int) row number to check)
# Returns:
# 		(boolean) True if the square contains a white pawn. False otherwise
def isWhitePawn(game_state, column, row):
        #gameState function is called to return a two-character string. The second character of that string is analyzed for the piece type
        if game_state[column][row] == "P":
                return True
        else:
                return False
# This function checks if a square is occupied by a black pawn
# Parameters:
# 		game_state: (list) the game_state
# 		column: (integer) column number to check
# 		row: (integer) row number to check)
# Returns:
# 		(boolean) True if the square contains a black pawn. False otherwise
def isBlackPawn(game_state, column, row):
        if game_state[column][row] == "p":
                return True
        else:
                return False
                
# This function checks if a square is occupied by a knight
# Parameters:
# 		game_state: (list) the game_state
# 		column: (integer) column number to check
# 		row: (integer) row number to check)
# Returns:
# 		(boolean) True if the square contains a knight. False otherwise                                                                                                       
def isKnight(game_state, column, row):
        #gameState function is called to return a two-character string. The second character of that string is analyzed for the piece type
        if game_state[column][row] == "k" or game_state[column][row] == "K":
                return True
        else:
                return False

# Figures out the column number of any pawn that's made it to the other side of the board. Returns -1 if none have 
# Parameters:
# 		game_state: (list) the game_state
# 		player: (integer) 0 to represent the CPU, 1 to represent the player
# Returns:
# 		column: (integer) Column number a crossed-over pawn is found on. -1 if none is found
def pawnCrossColumn(game_state, player):
        column = -1
        #Black is represented by 0
        if player == 0:
                for i in range(5):
                        if game_state[i][4] == "p":
                                column = i
        #White is represented by 1
        if player == 1:
                for i in range(5):
                        if game_state[i][0] == "P":
                                column = i
        return column               

# This function counts how many knights remain for a player, to see if a pawn can be converted into one
# Parameters:
# 		game_state: (list) the game_state
# 		player: (integer) 0 to represent the CPU, 1 to represent the player
# Returns:
# 		knights: (integer) Number of knights found for a player
def countKnights(game_state, player):
        knights = 0
        #Black is represented by 0
        if player == 0:
                for i in range(5):
                        for j in range(5):
                                if game_state[i][j] == "k":
                                        knights += 1
        #White is represented by 1
        if player == 1:
                for i in range(5):
                                for j in range(5):
                                        if game_state[i][j] == "K":
                                                knights += 1
        return knights  
# This function allows the player to choose the difficulty setting of the CPU
# Returns:
# 		difficulty: (string) a global variable that will contain the difficulty
# Parameters:
#		None
def difficultySetting():
	global difficulty
	print("'h' for Hard")
	print("'m' for medium")
	print("'e' for easy")
	print("\n")
	setting = False
	while setting == False:
		difficulty = input("Please enter the difficulty setting: ")	
		difficulty = difficulty.lower()
		if ('e' in difficulty) or ('m' in difficulty) or ('h' in difficulty):
			setting = True
			return difficulty
		else:
			print("Please enter a valid difficulty.")

        
# This function takes the game_state and evaluates what move best works in the computer's favour. The move is then returned as a list
# Parameters:
# 		game_state: (list) the game_state
# Returns:
# 		move_to_return: (list) Four integers representing the player's move.
#                                      First item represents the starting x-coordinate of the move
#                                      Second item represents the starting y-coordinate of the move
#                                      Third item represents the ending x-coordinate of the move
#                                      Fourth item represents the ending y-coordinate of the move      
def determineMove(game_state):
        max_point_value = 0
        move_collection = []
        for i in range(5):
                for j in range(5):
                        if game_state[i][j] == 'p' or game_state[i][j] == 'k':
                                for k in range(5):
                                        for l in range(5):
                                                if isValidMove(game_state, 0, i, j, k, l):
                                                        move_point_value = moveValueCalc(game_state, i, j, k, l)
                                                        if move_point_value > max_point_value:
                                                                max_point_value = move_point_value
                                                                move_collection = [i] + [j] + [k] + [l]                                                               
                                                        elif move_point_value == max_point_value:
                                                                move_collection += [i] + [j] + [k] + [l]
        num_of_moves = len(move_collection)/4
        move_num = random.randrange(num_of_moves)
        move_to_return = move_collection[(move_num*4):((move_num+1)*4)]
        return move_to_return
        
# This function takes the game_state and evaluates what teleport choice best works in the computer's favour. The move is then returned as a list
# Parameters:
# 		game_state: (list) the game_state
# Returns:
# 		move_to_return: (list) Two integers representing the player's move.
#                                     First item represents the x-coordinate of the teleport
#                                     Second item represents the y-coordinate of the teleport         
def determineTeleportChoice(game_state):
        max_point_value = 0
        move_collection = []
        
        for i in range(5):
                #Only goes to row 4
                for j in range(4):
                        if game_state[i][j] == ".":
                                move_point_value = teleportValueCalc(game_state, i, j)
                                #If the move_point_value is the highest so far...
                                if move_point_value > max_point_value:
                                        #max_point_value is updated
                                        max_point_value = move_point_value
                                        #move_collection is started anew with this move
                                        move_collection = [i] + [j]
                                #If it's equal to the highest value so far, it is added to move_collection
                                elif move_point_value == max_point_value:
                                        move_collection += [i] + [j]
                                #If move_point_value < max_point_value, it's ignored
                                                
        #Now, for moves of equal point value, a random one is chosen
        num_of_moves = len(move_collection)/2
        #Random move number chosen
        move_num = random.randrange(num_of_moves)
        #Move is extracted from move_collection
        move_to_return = move_collection[(move_num * 2): ((move_num + 1) * 2)]

        return move_to_return

# This function to evaluate a possible teleport choice's strategic value
# Parameters:
# 		game_state: (list) the game_state
# 		x: (float) the x-coordinate of the potential teleport choice
# 		y: (float) the y-coordinate of the potential teleport choice
# Returns:
# 		points: (integer) A value representing the relative worth of a potential move, to be compared to other possible moves
def teleportValueCalc(game_state, x, y):
        points = 0

        #Points added if it can attack piece to right
        if x <= 3: 
                if game_state[x + 1][y + 1] == 'P' or game_state[x + 1][y + 1] == 'K':
                        points += 2
        #Points added if it can attack piece to right
        if x >= 1:
                if game_state[x - 1][y + 1] == 'P' or game_state[x - 1][y + 1] == 'K':
                        points += 2
        #If it can attack pieces AND gets to teleport again after, this is a pretty good move, so 3 points added
        if points > 2 and y == 3:
                points += 3
        #Finally, if it can move ahead one after teleporting (in other words, will not be blocked by another piece in a future move), 1 point is added
        if game_state[x][y + 1] == '.':
                points += 1

        return points
        
# This function to evaluate if a piece is in danger from an enemy pawn
# Parameters:
# 		game_state: (list) the game_state
# 		x: (float) the x-coordinate of the piece's position
# 		y: (float) the y-coordinate of the piece's position
# Returns:
# 		danger: (boolean) Whether the piece is indeed in danger from pawns
def inDangerFromPawns(game_state, x, y):
        danger = False
        if difficulty == 'e':
                danger = False
        if difficulty == 'm':
                if (x <=3 and y<=3):
                        if game_state[x + 1][y + 1] == 'P':
                                cointoss = random.randrange(0,2)
                                if cointoss == 0:
                                        danger = True
                                else:
                                        danger = False
                if (x >= 1 and y <= 3):
                         if game_state[x - 1][y + 1] == 'P':
                                 cointoss = random.randrange(0,2)
                                 if cointoss == 0:
                                         danger = True
                                 else:
                                         danger = False
        #Makes sure it's not looking for attacking pawns outside of the game board
        if x <= 3 and y <= 3: 
                if game_state[x + 1][y + 1] == 'P':
                        danger = True
        #Makes sure it's not looking for attacking pawns outside of the game board
        if x >= 1 and y <= 3:
                if game_state[x - 1][y + 1] == 'P':
                        danger = True
                
        return danger

# This function to evaluate if a piece is in danger from an enemy knight
# Parameters:
# 		game_state: (list) the game_state
# 		x: (float) the x-coordinate of the piece's position
# 		Y: (float) the y-coordinate of the piece's position
# Returns:
# 		danger: (boolean) Whether the piece is indeed in danger from knights  
def inDangerFromKnights(game_state, x, y):
        danger = False

        #Until we can use arrays, this provides -2, -1, 0(removed below), 1, and 2 as horizontal values to test
        for i in range(-2, 3):
                #determines the number of vertical spaces to "move"
                vertical = 3 - abs(i)
                #If i == 0, it will only check the current square the piece is residing on, which never has an enemy knight by design
                if i == 0:
                        vertical = 0
                if difficulty == 'e':
                        danger = False
                if difficulty == 'm':
                        if x + i <= 4 and x + i >= 0 and y + vertical <= 4 and y + vertical >= 0:
                                if game_state[x + i][y + vertical] == 'K':
                                        cointoss = random.randrange(0,2)
                                        if cointoss == 0:
                                                danger = True
                                        else:
                                                danger = False
                        if x + i <= 4 and x + i >= 0 and y - vertical <= 4 and y - vertical >= 0:
                                if game_state[x + i][y - vertical] == 'K':
                                        cointoss = random.randrange(0,2)
                                        if cointoss == 0:
                                                danger = True
                                        else:
                                                danger = False
                #Makes sure it's not looking for attacking knights outside of the game board
                if x + i <= 4 and x + i >= 0 and y + vertical <= 4 and y + vertical >= 0: 
                        if game_state[x + i][y + vertical] == 'K':
                                danger = True
                #Makes sure it's not looking for attacking knights outside of the game board
                if x + i <= 4 and x + i >= 0 and y - vertical <= 4 and y - vertical >= 0: 
                        if game_state[x + i][y - vertical] == 'K':
                                danger = True
                

        return danger

# This function to evaluate if a piece is in danger from enemy pieces
# Parameters:
# 		game_state: (list) the game_state
# 		x: (float) the x-coordinate of the piece's position
# 		Y: (float) the y-coordinate of the piece's position
# Returns:
# 		inDangerFromKnights(game_state, x, y), inDangerFromPawns(game_state, x, y): (boolean) Whether the piece is indeed in danger   
def inDanger(game_state, x, y):
        return inDangerFromKnights(game_state, x, y) or inDangerFromPawns(game_state, x, y)

# This function to evaluate a possible move's strategic value
# Parameters:
# 		game_state: (list) the game_state
# 		x1: (integer) the x-coordinate of the potential starting square
# 		y1: (integer) the y-coordinate of the potential starting square
# 		x2: (integer) the x-coordinate of the potential ending square
# 		y2: (integer) the y-coordinate of the potential ending square
# Returns:
# 		points: (integer) A value representing the relative worth of a potential move, to be compared to other possible moves 
def moveValueCalc(game_state, x1, y1, x2, y2):
        points = 0
        if game_state[x2][y2] == 'P':
                points += 5
        if inDanger(game_state, x1, y1):
                if game_state[x1][y1] == 'p':
                        if difficulty == 'e':
                                points += 0
                        elif difficulty == 'm':
                                points += 3
                        else:
                                points += 5
                else:
                        if difficulty == 'e':
                                points += 0
                        else:
                                points += 1
        if game_state[x2][y2] == 'K':
                if difficulty == 'e':
                        points += 0
                elif difficulty == 'm':
                        points += 2
                else:
                        points += 3

        #The below, commented out, is an idea we can develop if we have more time
        '''if setUpNextCapture(game_state, x2, y2):
                points += 1'''
                
        return points

    

#---------------------------------------------------------THIS PART CHECKS MOVES-------------------------------------
# This function to evaluate if a move is valid/allowed
# Parameters:
# 		game_state: (list) the game_state
# 		start_column: (integer) the x-coordinate of the starting square
# 		start_row: (integer) the y-coordinate of the starting square
# 		moveto_column: (integer) the x-coordinate of the ending square
# 		moveto_row: (integer) the y-coordinate of the ending square
# Returns:
# 		valid_move: (boolean) Whether the move is valid
def isValidMove(game_state, player, start_column, start_row, moveto_column, moveto_row):
        valid_move = False
        if game_state[start_column][start_row] == 'P':
                if game_state[moveto_column][moveto_row] != "P" and game_state[moveto_column][moveto_row] != "K":
                        if start_column == moveto_column and moveto_row == (start_row - 1) and game_state[moveto_column][moveto_row] == ".":
                                valid_move = True
                        elif diagonalPawnMove(game_state, moveto_column,moveto_row,start_column,start_row):
                                valid_move = True

        elif isBlackPawn(game_state, start_column, start_row):
                if start_column == moveto_column and moveto_row == (start_row + 1) and game_state[moveto_column][moveto_row] == ".":
                        valid_move = True
                elif diagonalPawnMove(game_state, moveto_column,moveto_row,start_column,start_row):
                        valid_move = True

        if isKnight(game_state, start_column, start_row):
                if start_column >=0 and start_row <= 4 and start_column <= 4  and moveto_row >= 0 and moveto_row <= 4 and moveto_column >= 0 and moveto_column <= 4:
                        if (start_column - 2) == moveto_column:
                                if (start_row - 1) == moveto_row:
                                        valid_move = True
                                elif (start_row + 1) == moveto_row:
                                        valid_move = True
                        elif (start_column + 2) == moveto_column:
                                if (start_row - 1) == moveto_row:
                                        valid_move = True
                                elif (start_row + 1) == moveto_row:
                                        valid_move = True
                        elif (start_column - 1) == moveto_column:
                                if (start_row - 2) == moveto_row:
                                        valid_move = True
                                if (start_row + 2) == moveto_row:
                                        valid_move = True
                        elif (start_column + 1) == moveto_column:
                                if (start_row - 2) == moveto_row:
                                        valid_move = True
                                if (start_row + 2) == moveto_row:
                                        valid_move = True

        #Makes sure player cannot move another team's pieces
        if bool(player) != game_state[start_column][start_row].isupper():
                valid_move = False
        #Checks range for all pieces, rather than just knights
        if not(start_column >=0 and start_row <= 4 and start_column <= 4  and moveto_row >= 0 and moveto_row <= 4 and moveto_column >= 0 and moveto_column <= 4):
                valid_move = False

        start_cell_state = game_state[start_column][start_row]
        end_cell_state = game_state[moveto_column][moveto_row]

        #Makes sure pieces cannot move to squares occupied by pieces of the same colour
        if end_cell_state != "." and start_cell_state.isupper() == end_cell_state.isupper():
                valid_move = False

        return valid_move


# This function to check if pawns have made it to the other side, and what to do if they have
# Parameters:
# 		game_state: (list) the game_state
# 		line_turtle: (turtle) turtle to draw a move-displaying line
# Returns:
# 		temp_state: (list) The current game state after modification
def checkForSpecialPawnMoves(game_state, line_turtle):
        temp_state = copy.deepcopy(game_state)
        global teleport_w_pawn
        global teleport_b_pawn
        teleport_w_pawn = False
        teleport_b_pawn = False
        #pawnCrossColumn returns -1 if no pawns have crossed over, and otherwise returns the column number of a pawn that has
        #1 is used as a parameter to clarify that we are asking for white
        if pawnCrossColumn(temp_state, 1) != -1:
                if countKnights(temp_state, 1) < 2:
                        #If a player has less than two knights, the pawn is converted into one
                        temp_state[pawnCrossColumn(temp_state, 1)][0] = "K"
                else:
                        #Otherwise, the pawn gets moved to a new location
                        teleport_w_pawn = True
        #pawnCrossColumn returns -1 if no pawns have crossed over, and otherwise returns the column number of a pawn that has
        #0 is used as a parameter to clarify that we are asking for white
        if pawnCrossColumn(temp_state, 0) != -1:
                if countKnights(temp_state, 0) < 2:
                        #If a player has less than two knights, the pawn is converted into one
                        temp_state[pawnCrossColumn(temp_state, 0)][4] = "k"
                else:
                        #Otherwise, the pawn gets moved to a new location
                        teleport_b_pawn = True
        
        return temp_state

# This function checks to see if a pawn is able to move diagonally (eat a piece of the opponent)
# Parameters:
# 		game_state: (list) the current game state of the game
# 		moveto_column: (integer) the column the pawn is suppose to be moved
# 		moveto_row: (integer) the row the pawn is suppose to be moved
# 		start_column: (integer) the starting column of the piece selected
# 		start_row: (integer) the starting row of the piece selected
# Returns:
# 		(boolean) returns true if there is a pawn present diagonally
def diagonalPawnMove(game_state, moveto_column, moveto_row, start_column, start_row):
        if game_state[start_column][start_row] == "P":
                if abs(moveto_column - start_column) == 1:
                        if moveto_row == (start_row - 1):
                                if game_state[moveto_column][moveto_row] == "k" or game_state[moveto_column][moveto_row] == "p":
                                        return True
                                else:
                                        return False
                        else:
                                return False
                else:
                                return False
        elif game_state[start_column][start_row] == "p":
                if abs(moveto_column - start_column) == 1:
                        if moveto_row == (start_row +1):
                                if game_state[moveto_column][moveto_row] == "K" or game_state[moveto_column][moveto_row] == "P":
                                        return True
                                else:
                                        return False
                        else:
                                return False
                else:
                                return False
        else:
                return False

# This function checks to see where the user click input is on the board and returns the coordinates of that user click input
# Parameters: 
# 		x: (float) the column value of the user click input
# 		y: (float) the row value of the user click input
# Returns:
# 		grid_area: (list) returns the corresponding grid coordinates the user clicked 
def returnCoordinate(x, y):
        grid_area = []
        if x > 0 and x <= 60:
                grid_area += [0]
        elif x > 60 and x <= 120:
                grid_area += [1]
        elif x > 120 and x <= 180:
                grid_area += [2] 
        elif x > 180 and x <= 240:
                grid_area += [3]
        elif x > 240 and x <= 300:
                grid_area += [4]
        if y > 0 and y <= 60:
                temp_string = grid_area + [4]
                grid_area = temp_string
        elif y > 60 and y <= 120:
                temp_string = grid_area + [3]
                grid_area = temp_string
        elif y > 120 and y <= 180:
                temp_string = grid_area + [2]
                grid_area = temp_string
        elif y > 180 and y <= 240:
                temp_string = grid_area + [1]
                grid_area = temp_string
        elif y > 240 and y <= 300:
                temp_string = grid_area + [0]
                grid_area = temp_string 
        return grid_area

                                        
#----------------------------------------------------THIS PART APPLIES PENALTIES------------------------------------------------------
# This function applies a penalty point if the user made an invalid move
# Parameters:
# 		game_state: (list) the current game state of the game
# 		player: (integer) the player who is going to receive a penalty point (0 for AI, 1 for user)
# Returns:
# 		temp_state: (list) returns the current game state with the penalty point implemented
def applyPenPoint(game_state, player):
        temp_state = copy.deepcopy(game_state)
        notifier.clear()
        if player == 0:
                temp_state[5] += 1
                notifier.write("Penalty point applied for CPU.")

        else:
                temp_state[6] += 1
                notifier.write("You have received a penalty point.")

        return temp_state


#-------------------------------------------UPDATING LAYOUT(WHAT USER SEES)----------------------------------------------------------
# This function updates the screen that is being displayed to the user
# Parameters: 
# 		game_state: (list) the current game state of the game
# 		piece_drawer: (turtle) the turtle that is used to draw the pieces
# Returns:
# 		None
def updateScreen(game_state, piece_drawer):
        #First, the board is cleared
        piece_drawer.clear()

        piece_drawer.shape("bpawn.gif")
        stamping(game_state, piece_drawer, "p")
        piece_drawer.shape("bknight.gif")
        stamping(game_state, piece_drawer, "k")

        piece_drawer.shape("wpawn.gif")
        stamping(game_state, piece_drawer, "P")
        piece_drawer.shape("wknight.gif")
        stamping(game_state, piece_drawer, "K")
                

# This function draws the line where the turtle has moved
# Parameters:
# 		line_turtle: (turtle) the turtle that tells the user where the piece has moved to
# 		x_start: (integer) the starting column of the piece selected
# 		y_start: (integer) the starting row of the piece selected
# 		x_end: (integer) the ending column of the piece selected
# 		y_end: (integer) the ending row of the piece selected
# Returns:
# 		None
def lineDraw(line_turtle, start_x, start_y, end_x, end_y):
        line_turtle.penup()              
        line_turtle.goto(coordinates(start_x, start_y))
        line_turtle.pendown()
        line_turtle.goto(coordinates(end_x, end_y))  
                
# This function stamps every place a piece with the same ending as "code" appears
# Parameters:
# 		game_state: (list) the current game state of the game
# 		piece_drawer: (turtle) the turtle that is used to draw the pieces
# 		code: (string) the type of piece that is being stamped
# Returns:
# 		None
def stamping(game_state, piece_drawer, code):
        for i in range(5):
                for j in range(5):
                        cell_state = game_state[i][j]
                        if cell_state == code:
                                piece_drawer.goto(coordinates(i, j))
                                piece_drawer.stamp()

                                
# This function takes pawns that have reached the other side of the game board anywhere on the board (as long as its not occupied)
# If a pawn has reached the other side and is not converted into a knight, it is moved
# Parameters:
# 		game_state: (list) the current game state of the game
# 		b_case: (boolean) if a black piece has reached the other side of the board
# 		w_case: (boolean) if a white piece has reached the other side of the board
# 		line_turtle: (turtle) the turtle that tells the user where the piece has moved to
# 		x: (float) the column value of the user click input
# 		y: (float) the row value of the user click input
# Returns:
# 		temp_state: (list) returns the current game state of the game with the teleported pawn
def teleportPawns(game_state, b_case, w_case, line_turtle, x, y):
        temp_state = copy.deepcopy(game_state)  
        cur_black_col = pawnCrossColumn(temp_state, 0)
        cur_white_col = pawnCrossColumn(temp_state, 1)
        '''NOTE: need to find out what the game rules are if you simply move to another column but the same row!'''
        if not (b_case and w_case):
                if b_case:
                        valid_input = False
                        
                        move_input = determineTeleportChoice(temp_state)
                        move_x = move_input[0]
                        move_y = move_input[1]
                        

                        #Line drawn to new location        
                        line_turtle.clear()
                        lineDraw(line_turtle, cur_black_col, 4, move_x, move_y)             

                        #game_state updated
                        temp_state[move_x][move_y] = "p"
                        temp_state[cur_black_col][4] = "."

                if w_case:
                        notifier.clear()
                        #Keeps prompting until user enters a valid square
                        #Not sure if instead should be penalty-based?
                        move_input = returnCoordinate(x,y)
                        move_x = move_input[0]
                        move_y = move_input[1]
                        #move_input = input("Choose an empty square to move your pawn to.")
                        taking_teleport = True

                        #Line drawn to new location        
                        line_turtle.clear()
                        lineDraw(line_turtle, cur_white_col, 0, move_x, move_y) 
                        
                        #game_state updated
                        temp_state[move_x][move_y] = "P"
                        temp_state[cur_white_col][0] = "."

        elif b_case and w_case:
                #If both pawns are teleporting, black gets moved "first"
                move_input = determineTeleportChoice(temp_state)
                move_x = move_input[0]
                move_y = move_input[1]
                bm_x = move_x
                bm_y = move_y

                #Game state is updated for white's move
                temp_state[move_x][move_y] = "p"
                temp_state[cur_black_col][4] = "."


                #Now for moving white
                valid_input = False
                notifier.clear()
                #Keeps prompting until user enters a valid square
                                                                #Not sure if instead should be penalty-based?

                move_input = returnCoordinate(x,y)
                move_x = move_input[0]
                move_y = move_input[1]
                wm_x = move_x
                wm_y = move_y


                #If it collides with another teleporting pawn, both are removed
                                #Not sure if this is the rule?
                if temp_state[move_x][move_y] == "p":
                        temp_state[move_x][move_y] = "."
                else:
                        temp_state[move_x][move_y] = "P"

                #Now the game state is updated for white's move
                temp_state[cur_white_col][0] = "."

                
                #Line drawn to new locations       
                line_turtle.clear()
                lineDraw(line_turtle, cur_black_col, 4, bm_x, bm_y) 
                lineDraw(line_turtle, cur_white_col, 0, wm_x, wm_y)             
                                
        return temp_state

#----------------------------------------------------GAME STATES------------------------------------------------
# This function takes the game state and extracts the state of a certain cell, returning the resulting 2-character string
# Parameters:
# 		game_state: (list) the current game state of the game
# 		wcolumn: (integer)the starting column of a white piece
# 		wrow: (integer) the starting row of a white piece
# 		wmove_column: (integer) the ending column of a white piece
# 		wmove_row: (integer) the ending row of a white piece
# 		bcolumn: (integer) the starting column of a black piece
# 		brow: (integer) the starting row of a black piece
# 		bmove_column: (integer) the ending column of a black piece
# 		bmove_row: (integer) the ending row of a black piece
# Returns: 
# 		temp_state: (list) returns the current game state of the game
def updateGameState(game_state, wcolumn, wrow, wmove_column, wmove_row, bcolumn, brow, bmove_column, bmove_row):
        temp_state = copy.deepcopy(game_state)
        if isValidMove(temp_state, 1, wcolumn, wrow, wmove_column, wmove_row) == False and isValidMove(temp_state, 0, bcolumn, brow, bmove_column, bmove_row)== False:
                temp_state = applyPenPoint(temp_state, 0)
                temp_state = applyPenPoint(temp_state, 1)
        elif isValidMove(temp_state, 1, wcolumn, wrow, wmove_column, wmove_row) == True and isValidMove(temp_state, 0, bcolumn, brow, bmove_column, bmove_row) == False:
                overwrite = temp_state[wcolumn][wrow]
                temp_state[wmove_column][wmove_row] = overwrite
                temp_state[wcolumn][wrow] = "."
                temp_state = applyPenPoint(temp_state, 0)
        elif isValidMove(temp_state, 0, bcolumn, brow, bmove_column, bmove_row) == True and isValidMove(temp_state, 1, wcolumn, wrow, wmove_column, wmove_row) == False:
                overwrite = temp_state[bcolumn][brow]
                temp_state[bmove_column][bmove_row] = overwrite
                temp_state[bcolumn][brow] = "."
                temp_state = applyPenPoint(temp_state, 1)
        elif isValidMove(temp_state, 0, bcolumn, brow, bmove_column, bmove_row) == True and isValidMove(temp_state, 1, wcolumn, wrow, wmove_column, wmove_row) == True:
                b_captured_slot = temp_state[bmove_column][bmove_row]
                w_m_piece = temp_state[wcolumn][wrow]
                b_m_piece = temp_state[bcolumn][brow]

                temp_state[wcolumn][wrow] = "."
                temp_state[bcolumn][brow] = "."

                temp_state[wmove_column][wmove_row] = w_m_piece

                b_captured_updated = temp_state[bmove_column][bmove_row]

                if b_captured_updated == b_captured_slot or (b_m_piece == "k" and b_captured_updated == "P") or b_captured_updated == ".":
                                temp_state[bmove_column][bmove_row] = b_m_piece
                elif b_m_piece.upper() == b_captured_updated:
                                temp_state[bmove_column][bmove_row] = "."

        return temp_state



#---------------------------------------------CHECKS IF GAME IS OVER AND WHO WON------------------------------------------
# This function determines if its game over already
# Parameters:
# 		game_state: (list) the current game state of the game
# Returns:
# 		game_over: (boolean) returns true or false depending on the game state
def isGameOver(game_state):
        game_over = False
        a = game_state[5]
        b = game_state[6]
        still_w_pawns = pawnState(game_state,"P")
        still_b_pawns = pawnState(game_state,"p")
        
        if not still_b_pawns or not still_w_pawns:
                game_over = True
        
        if (a == 2):
                game_over = True
        elif (b == 2):
                game_over = True

        return game_over

# This function checks the current game state and checks if someone won
# Parameters:
# 		game_state: (list) the current game state of the game
# Returns:
# 		None
def playerWin(game_state):
        pen_point_black = game_state[5]
        pen_point_white = game_state[6]
        still_w_pawns = pawnState(game_state,"P")
        still_b_pawns = pawnState(game_state,"p")

        if (isGameOver(game_state) == True):        
                if (pen_point_black == 2) and (pen_point_white == 2):
                        notifier.clear()
                        notifier.write("Draw, both pen points")
                elif (not still_w_pawns and not still_b_pawns):
                        notifier.clear()
                        notifier.write("Draw, both out of pawns")
                elif (pen_point_black == 2):
                        notifier.clear()
                        notifier.write("You win!, black pen point")
                elif (not still_b_pawns):
                        notifier.clear()
                        notifier.write("CPU is out of pawns, you win!")
                elif (pen_point_white == 2):
                        notifier.clear()
                        notifier.write("You have reached the maximum number of penalty points, CPU wins!")
                elif (not still_w_pawns):
                        notifier.clear()
                        notifier.write("You are out of pawns, CPU wins!")
                else:
                        notifier.clear()
                        notifier.write("Game is still in progress")    
            
            
# This function checks if the piece at a specific place in game state exists
# Parameters:
# 		game_state: (list) the original game state that can be checked to see if a specific pawn exists
# 		piece_to_find: (string) either "P" for white pawns or "p" for black pawns
# Returns:
# 		still_pawn: (boolean) returns true if the specified pawn exists in a certain place in the game state
def pawnState(game_state,piece_to_find):
        still_pawns = False
        for i in range(5):
                for j in range(5):
                        if game_state[i][j] == piece_to_find:
                                still_pawns = True
        return still_pawns


#--------------------------------------------------MAIN AND USER INPUT-------------------------------------------   
# This function displays the rules of the game if the user chooses to
# Parameters:
# 		None
# Returns:
# 		None
def printRules():
        print("\nApocalypse is a variant of chess where each side has only 5 pawns and 2 knights")
        print("\nThe rules of the game include:")
        print(" - The objective is to remove the other sides pawns without losing your own")
        print(" - If you make a mistake you will be given a penalty point, the player loses \n if they recieve 2 penalty points")
        print(" - Both pawns and knights move as they normally would in regular chess")
        print(" - If a pawn reaches the end of the board and both knights are still in play,\n you may choose any square on the board to move that piece as long as it is")
        print(" not occupied by another piece of either team. If you are missing 1 or more\n knights, then that pawn becomes a knight")
        print(" - If two pieces move to the same tile at the same time, a horseman captures\n a pawn and same-type pieces are both removed")
        print(" - If a capture is attempted on a piece and it moves from that tile then then\n it still remains in play")

		
# This function displays the hotkeys for the user to access
# Parameters:
# 		None
# Returns:
# 		None		
def printHotkeys():
        print("\nPress the following hotkeys while in game to perform the following actions: ")
        print(" s - saves the current game")
        print(" l - loads the current game")
        print(" n - starts a new game")
        print(" r - prints the rules\n")
        
# This function makes the AI pick a valid move
# Parameters:
# 		game_state: (list) the original game state is uploaded in the function so that it can be modified
# 		piece_drawer: (turtle) the turtle that is used to draw the pieces
# 		line_turtle: (turtle) the turtle that tells the user where the piece has moved to
# 		x_start: (integer) the starting column of the piece selected
# 		y_start: (integer) the starting row of the piece selected
# 		x_end: (integer) the ending column of the piece selected
# 		y_end: (integer) the ending row of the piece selected
# Returns:
# 		temp_state: (list) returns the current game state with the AI move implemented
def userMoveDisplay(game_state, piece_drawer, line_turtle, x_start, y_start, x_end, y_end):
        temp_state = copy.deepcopy(game_state)
        computer_move = determineMove(temp_state)
        line_turtle.clear()


        if isValidMove(temp_state, 1, x_start, y_start, x_end, y_end):
                lineDraw(line_turtle, x_start, y_start, x_end, y_end)

        cpu_x_start = computer_move[0]
        cpu_y_start = computer_move[1]
        cpu_x_end = computer_move[2]
        cpu_y_end = computer_move[3]             

        if isValidMove(temp_state,0,cpu_x_start, cpu_y_start, cpu_x_end, cpu_y_end):
                lineDraw(line_turtle, cpu_x_start, cpu_y_start, cpu_x_end, cpu_y_end)

        temp_state = updateGameState(temp_state, x_start, y_start, x_end, y_end, cpu_x_start, cpu_y_start, cpu_x_end, cpu_y_end)

        updateScreen(temp_state, piece_drawer)

        return temp_state
        
        
# This function checks to see if the user click input is within range of the game board.
# Parameters:
# 		x: (float) the column value of the user click input
# 		y: (float) the row value of the user click input 
# Returns:
# 		x: (Boolean) checks to see if x is within range. Returns True if it is.
# 		y: (Boolean) checks to see if y is within range. Returns True if it is.
def inRange(x,y):
        return x > 0 and x < WIDTH and y > 0 and y < WIDTH
        
# This function accepts the user click input, checks the move, and makes the move
# Parameters:
# 		x: (float) the column value of the user click input
# 		y: (float) the row value of the user click input 
# Returns:
# 		None
def gameClickHandler(x, y):
        global start_x
        global start_y
        global game_state
        global game_over
        global piece_selected
        global taking_teleport
        global piece_drawer
        global line_turtle
        global valid_teleport
        global event_in_progress
        
        temp_state = copy.deepcopy(game_state)
        
        if inRange(x,y) and not event_in_progress:
                column_and_row = returnCoordinate(x,y)
                column_num = column_and_row[0]
                row_num = column_and_row[1]
                
                if not game_over and taking_teleport:
                        end_pos = returnCoordinate(x, y)
                        end_x = end_pos[0]
                        end_y = end_pos[1]
                        if game_state[end_x][end_y] == ".":
                                event_in_progress = True
                                game_state = teleportPawns(game_state, teleport_b_pawn, teleport_w_pawn, line_turtle, x, y)
                                notifier.clear()
                                updateScreen(game_state, piece_drawer)
                                taking_teleport = False
                                event_in_progress = False
                        
                
                elif not game_over and game_state[column_num][row_num] in "PK" and not taking_teleport:
                        start_pos = returnCoordinate(x,y)
                        start_x = start_pos[0]
                        start_y = start_pos[1]
                        piece_selected = True
        
                elif not game_over and piece_selected:
                        event_in_progress = True
                        end_pos = returnCoordinate(x,y)
                        end_x = end_pos[0]
                        end_y = end_pos[1]
                        
                        game_state = userMoveDisplay(game_state, piece_drawer, line_turtle, start_x, start_y, end_x, end_y)
                        game_over = isGameOver(game_state)
                        piece_selected = False

                        #deepcopy needed for the nested lists to clone
                        old_state = copy.deepcopy(game_state)

                        #Carrying out actions on pawns that have moved to the other side is complex
                        game_state = checkForSpecialPawnMoves(game_state, line_turtle)
                        
                        #Only updates the game_state checkForSpecialPawnMoves if it looks different
                        if game_state != old_state:
                                updateScreen(game_state, piece_drawer)

                        #game_over has to be evaluated again in case a player's lost a pawn through checkForSpecialPawnMoves
                        game_over = isGameOver(game_state)  # function name depends on Tyler
                        
                        if game_over:
                                playerWin(game_state)
                        elif teleport_w_pawn or teleport_b_pawn:
                                if teleport_b_pawn and not teleport_w_pawn:
                                        game_state = teleportPawns(game_state, teleport_b_pawn, teleport_w_pawn, line_turtle, x, y)
                                        updateScreen(game_state, piece_drawer)
                                else:
                                        taking_teleport = True
                                        notifier.write("\nYour pawn has moved to the other side of the board.\nChoose an empty square to move your pawn to.")
                        event_in_progress = False
						
						
# This functions saves the game state into a .txt file called savegame.txt
# Parameters:
# 		None
# Returns:
# 		None						
def saveHandler():
        if not game_over:
                write_file  = open("savegame.txt", "w")

                if taking_teleport == True:
                        write_file.write("1\n")
                else:
                        write_file.write("0\n")

                for i in range (5):
                        for j in range (5):
                                write_file.write(game_state[i][j] + " ")
                        write_file.write("\n")
                write_file.write(str(game_state[5]) + "\n")
                write_file.write(str(game_state[6]) + "\n")
                notifier.clear()
                notifier.write("Save completed.")
                write_file.close()

        else:
                notifier.clear()
                notifier.write("Cannot save.")

# This functions loads the saved game
# Parameters:
# 		None
# Returns:
# 		None 
def loadHandler():
        global game_state
        global game_over
        global taking_teleport
        global line_turtle
        global event_in_progress
        
        if not event_in_progress:
                event_in_progress = True
                try:
                        load_file = open("savegame.txt", "r")
                        temp_list = []
                        teleport_line = load_file.readline()
                        assert(teleport_line[0] in "01")
                        if "1" in teleport_line:
                                taking_teleport = True
                                notifier.write("Choose an empty square to move your pawn to.")
                        else:
                                taking_teleport = False
                        for i in range (5):
                                line = load_file.readline() 
                                pieces = line.split()
                                column_list = []
                                for j in range (5):
                                        #Piece has to be a valid piece type. The len argument makes sure that the string is also not something
                                        #       like "pk", which would still satisfy "in 'pkPK.'"
                                        assert(pieces[j] in "pkPK." and len(pieces[j]) == 1)
                                        column_list.append(pieces[j])
                                temp_list.append(column_list)
                        pen_string_1 = load_file.readline()
                        temp_list.append(int(pen_string_1))
                        pen_string_2 = load_file.readline()
                        temp_list.append(int(pen_string_2))
                        assert(temp_list[5] in range(0,3) and temp_list[6] in range(0,3))
                        game_state = temp_list
                        line_turtle.clear()
                        updateScreen(game_state, piece_drawer)
                        if taking_teleport:
                                checkForSpecialPawnMoves(game_state, line_turtle)
                        game_over = isGameOver(game_state)
                        if game_over:
                                playerWin(game_state)
                        notifier.clear()
                        notifier.write("\nGame loaded.")
                        print(game_state[5], game_state[6])
                #If the user has never saved a game yet...
                except IOError:
                        notifier.clear()
                        notifier.write("No saved state to load.")
                #If info is removed from the game file, or it's blank...
                except IndexError:
                        notifier.clear()
                        notifier.write("Something wrong with save file. Could not load.")
                #If save file is rewritten manually, like all 'p's replaced with 'q's...
                except AssertionError:
                        notifier.clear()
                        notifier.write("Something wrong with save file. Could not load.")
                #If converting penalty point lines into ints does not work...
                except ValueError:
                        notifier.clear()
                        notifier.write("Something wrong with save file. Could not load.")
                event_in_progress = False
        else:
                notifier.clear()
                notifier.write("Please wait until the current event is finished to load a game.")

                
# This function sets up a new game 
# Parameters:
# 		None
# Returns:
# 		None				
def setUpNewGame():
        global event_in_progress
        if not event_in_progress:
                piece_drawer.clear()
                line_turtle.clear()

                notifier.clear()

                global game_state
                #The game state at the beginning of the game is written out
                #game_state = "00.k.p...P.K.p.......P.p.......P.p.......P.k.p...P.K"
                game_state = [["k","p",".","P","K"],["p",".",".",".","P"],["p",".",".",".","P"],["p",".",".",".","P"],["k","p",".","P","K"],0,0]

                '''Alternate game states for testing'''
                #game_state = [[".","p",".","P","."],["P",".",".",".","p"],["p",".",".",".","P"],["p",".",".",".","P"],["k","p",".","P","K"],0,0]

                #piece_drawer will be resized; WIDTH/250 returns a value that looks nice
                new_size = WIDTH/250
                piece_drawer.turtlesize(new_size, new_size)

                difficulty = ""
                difficultySetting()
                printHotkeys()
                #The pieces are drawn onto the board
                updateScreen(game_state, piece_drawer)

                global game_over
                global taking_teleport
                global piece_selected
                global event_in_progress
                
                event_in_progress = False
                piece_selected = False
                game_over = False
                taking_teleport = False
        
# This function is the main function. It makes the initial turtles such as the screen, the pieces, the line drawn.
# This function also makes the initial game state of the game 
# Parameters:
# 		None
# Returns:
# 		None
def main():
        #global wn
        wn = turtle.Screen()
        wn.register_shape("bknight.gif")
        wn.register_shape("bpawn.gif")
        wn.register_shape("wknight.gif")
        wn.register_shape("wpawn.gif")
        wn.title("Apocalypse")

        global piece_drawer
        #turtle for stamping out the board state
        piece_drawer = turtle.Turtle()
        piece_drawer.ht()
        piece_drawer.up()
        piece_drawer.speed(0)

        global line_turtle
        #line_turtle is created, and its attributes are set
        line_turtle = turtle.Turtle()
        line_turtle.color("green")
        line_turtle.pensize(3)
        line_turtle.ht()

        game_name = turtle.Turtle()
        drawWelcome(game_name, wn)
        
        drawGameBoard(wn)

        global event_in_progress
        
        event_in_progress = False

        setUpNewGame()

        #Tracer is reset
        wn.tracer(1)
        wn.onscreenclick(gameClickHandler)
        wn.onkey(saveHandler, "s")
        wn.onkey(loadHandler, "l")
        wn.onkey(setUpNewGame, "n")
        wn.onkey(printRules, "r")
        wn.listen()
        wn.mainloop()


        
main()

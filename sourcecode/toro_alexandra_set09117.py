import random
import copy
import sys
#Creating the board
board = [ [0, 1, 0, 1, 0, 1, 0, 1],
		  [1, 0, 1, 0, 1, 0, 1, 0],
		  [0, 1, 0, 1, 0, 1, 0, 1],
 		  [0, 0, 0, 0, 0, 0, 0, 0],
		  [0, 0, 0, 0, 0, 0, 0, 0],
		  [2, 0, 2, 0, 2, 0, 2, 0],
		  [0, 2, 0, 2, 0, 2, 0, 2],
 		  [2, 0, 2, 0, 2, 0, 2, 0]]
#Declaring variables
board_size=8  
y=0
playeR= 1
playerB=2
playerKR=3
playerKB=4
turn=0
#Converts numbers from the board into characters
def intToText(num):
	if(num == 0): 
		return ' '
	if(num == 1): 
		return 'r'
	if(num == 2): 
		return 'b'
	if(num==3):
		return 'R'
	if(num==4):
		return 'B'
#Prints the grid and updates the board if any pieces have been converted to a King during the last turn
def printGrid():
	CheckKing()
	print(' 0 1 2 3 4 5 6 7')
	print('┌─┬─┬─┬─┬─┬─┬─┬─┐')
	#Loops through the grid printing it
	for y in range(board_size):
		print('│' + intToText(board[y][0]) + '│' + intToText(board[y][1]) + '│' + intToText(board[y][2]) + '│' + intToText(board[y][3]) + '│' + intToText(board[y][4]) + '│' + intToText(board[y][5]) + '│' + intToText(board[y][6]) + '│' + intToText(board[y][7]) + '│'+' ' +str(y)+'\n'
	      '├─┼─┼─┼─┼─┼─┼─┼─┤')

	print('│0│1│2│3│4│5│6│7│')
	print('└─┴─┴─┴─┴─┴─┴─┴─┘')
	checkVictory()
#Controls turns checking between the computer and the user
def arcadeMode():
	if(turn==0):
		validateR()
	if (turn==1):
		validateAIB()
#Controls turns between two users changing the variable turn after they choose a move	
def twoPlayerMode():
	if(turn==0):
		validateR()
	if (turn==1):
		validateB()
def aiVSaiMode():
	if(turn==0):
		validateAIR()
	if (turn==1):
		validateAIB()
#Checks the coordinates given are valid
def validateR():
	#This variables are global so they can be used in other definitions
	global piece, pieceX, pieceY, move, moveX, moveY, board,turn, board2, copyBoard
	piece = input('\n' 'It is player Rs turn. Choose your piece to move or EXIT to quit:' '\n')
	if ( piece == 'help'):
	    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3,2) or EXIT to quit''\n')
	if (piece == "EXIT" or piece=='exit'):
		sys.exit()
	#Checks if the input is on the correct format and splits it into two X and Y variables
	if (len(piece) == 3):
		splitcord= piece.split(',')
		pieceX=int(splitcord[0])
		pieceY=int(splitcord[1])
		if(pieceX <8 and pieceX >=0 and pieceY <8 and pieceY >=0 ):	
			#Checks if the chosen piece belongs to the user
			if(board[pieceY][pieceX]== playeR or board[pieceY][pieceX]== playerKR):
				print('\n' 'Right piece!' '\n')
				#Stores board before and after the user moves the piece: used for Undo and Redo action
				copyBoard= board[:]
				copyBoard= copy.deepcopy(board)
				board2=board[:]
				#Depending of the selected piece legal moves will become avalible
				if(board[pieceY][pieceX]== playeR):
					possibleMovesR()
				if(board[pieceY][pieceX]== playerKR):
					possibleMovesRKing()
				undoRedo()	
			else:
				print('Cannot move this piece. Try again :)')
	else:
		print('Invalid input. Type \'help\' if you\'re stuck')
#Controls the Kings special moves
def possibleMovesRKing():
	#Making these values global so they can be used accross functions 
	global newPosX, newPosY, turn
	#Handles exception in case values checked are out of range
	try:
		#Checks if there's any empty gaps that the king can jump to after eating a piece
		if(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			#Checks in every direction if there's an enemy's piece that can be eaten
			if((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX-1]==playerKB) and pieceY+2<8 and pieceX-2>=0):
				#Updates board values
				board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY+2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpR()
				printGrid()
				#Changes turn to the other player
				turn=1
			if((board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB) and pieceY+2<8 and pieceX+2<8):
				board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX+1]=0
				newPosY=pieceY+2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
			if((board[pieceY-1][pieceX-1]==playerKB or board[pieceY-1][pieceX-1]==playerB) and pieceY-2>=0 and pieceX-2>=0):
				board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX-1]=0
				newPosY=pieceY-2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
			if((board[pieceY-1][pieceX+1]==playerKB or board[pieceY-1][pieceX+1]==playerB) and pieceY-2>=0 and pieceX+2<8):
				board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX+1]=0
				newPosY=pieceY-2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				printGrid()
				turn=1
		#Makes user aware there's no moves
		elif(((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB) or (board[pieceY+1][pieceX-1]==playerKB or board[pieceY+1][pieceX+1]==playerKB)) and (board[pieceY+2][pieceX+2]!=0 and board[pieceY+2][pieceX-2]!=0)):
			print('...but there is not legal moves available. Try again :D')
	except:
		pass
	try:	
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0 or board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0)and turn==0): 
			move=input('Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				#Divides input into two values or coordinates
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playeR):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if((moveY==pieceY+1 or moveY==pieceY-1) and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board values
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							#Prints grid and changes turn
							printGrid()
							turn=1
						else:
							print('This move is not allowed')

				else:
					print('A piece is already there!')
			#Will keep executing function till a valid value is written
			else:
				possibleMovesRKing()
	except:
		pass
def possibleMovesR():
	global newPosX, newPosY,turn
	#Handles exception incase values are out of range
	try:
		#Checks if the chosen piece has a enemy's piece nearby
		if(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0):
			if((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX-1]==playerKB) and pieceY+2<8 and pieceX-2>=0):
				#Updates board
				board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY+2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpR()
				#Changes turn to the other player
				turn=1		
			if((board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB) and pieceY+2<8 and pieceX+2<8):
				board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX+1]=0
				newPosY=pieceY+2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpR()
				turn=1
		#Makes user aware there's no moves
		elif(((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB) or (board[pieceY+1][pieceX-1]==playerKB or board[pieceY+1][pieceX+1]==playerKB)) and (board[pieceY+2][pieceX+2]!=0 and board[pieceY+2][pieceX-2]!=0)):
			print('...but there is not legal moves available. Try again :D')
	except:
		pass
	try:	
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0)and turn==0): 
			move=input('Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				#Divides input into two values or coordinates
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playeR):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY+1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board values
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							#Prints grid and changes turn
							printGrid()
							turn=1
						else:
							print('This move is not allowed')

				else:
					print('A piece is already there!')
			#Will keep executing function till a valid value is written
			else:
				possibleMovesR()
	except:
		pass
#Another jump will be taken if there's an enemy's piece to be eaten
def doubleJumpR():
	if(board[newPosY][newPosX]==playeR):
		#Checks that there's another immidiate enemy's piece and that the next square is an empty gap 
		while(((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB) and (board[newPosY+2][newPosX+2]==0)) or ((board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB) and (board[newPosY+2][newPosX-2]==0))):
			#Checks for left and right directions for a Black piece
			if(board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB) and pieceY+1<8 and pieceX-1>=0:
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX-1]=0
				printGrid()
			if(board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB) and pieceY+1<8 and pieceX+1<8:
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX+1]=0
				printGrid()	
	#If the piece that's being move is a King, enemy's pieces can be eaten backwards and forwards
	if(board[newPosY][newPosX]==playerKR):
		while(((board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB) and board[newPosY+2][newPosX-2]==0) or((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB) and board[newPosY+2][newPosX+2]==0) or((board[newPosY-1][newPosX-1]==playerB or board[newPosY-1][newPosX-1]==playerKB)and board[newPosY-2][newPosX-2]==0) or ((board[newPosY-1][newPosX+1]==playerB or board[newPosY-1][newPosX+1]==playerKB) and board[newPosY-2][newPosX+2]==0)):
			#Checks every direction for enemy's pieces
			if((board[newPosY+1][newPosX-1]==playerB or board[newPosY+1][newPosX-1]==playerKB)and pieceY+1<8 and pieceX-1>=0 ):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX-1]=0
				printGrid()
			if((board[newPosY+1][newPosX+1]==playerB or board[newPosY+1][newPosX+1]==playerKB)and pieceY+1<8 and pieceX+1<8):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX+1]=0
				printGrid()
			if((board[newPosY-1][newPosX-1]==playerB or board[newPosY-1][newPosX-1]==playerKB)and pieceY-1>=0 and pieceX-1>=0):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX-1]=0
				printGrid()
			if((board[newPosY-1][newPosX+1]==playerB or board[newPosY-1][newPosX+1]==playerKB)and pieceY-1>=0 and pieceX+1<8):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX+1]=0
				printGrid()
#Checks the coordinates given are valid
def validateB():
		#Makes these variables global so their values can be used by other functions
		global piece, pieceX, pieceY, move, moveX, moveY, board,turn,board2,copyBoard
		#Gives player options to move piece, exit the game or ask for help if the input is incorrect
		piece = input('\n' 'Its player B turn! Choose your piece to move or EXIT to quit:' '\n')
		if ( piece == 'help'):
		    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3,2) or EXIT to quit''\n')
		if(piece=='exit'or piece=='EXIT'):
			sys.exit()	
		#Checks if the input is on the correct format and splits it into two X and Y variables	    
		if (len(piece) == 3):
			splitcord= piece.split(',')
			pieceX=int(splitcord[0])
			pieceY=int(splitcord[1])
			if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
				#Checks if the chosen piece belongs to the user
				if(board[pieceY][pieceX]== playerB or board[pieceY][pieceX==playerKR]):
					print('\n''Right piece!''\n')
					#Stores board before and after the user moves the piece: used for Undo and Redo action
					copyBoard= board[:]
					copyBoard= copy.deepcopy(board)
					board2=board[:]
					if(board[pieceY][pieceX]== playerB):
						possibleMovesB()
					if(board[pieceY][pieceX]== playerKB):
						possibleMovesBKing()
					undoRedo()
				else:
					print('Cannot move this piece. Try again :)')
				
		else:
			print('Invalid input. Type \'help\' if you\'re stuck')
#Controls the Kings special moves
def possibleMovesBKing():
	#Making these values global so they can be used accross functions 
	global newPosX, newPosY, turn
	try:
		#Checks there's avalible spaces to jump over after taking a enemy's piece
		if(board[pieceY+2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			if((board[pieceY+1][pieceX-1]==playerKR or board[pieceY+1][pieceX-1]==playeR) and pieceY+2<8 and pieceX-2>=0):
				#Updates board
				board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY+2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpB()
				#Changes turn to the other player
				turn=0
			if((board[pieceY+1][pieceX+1]==playeR or board[pieceY+1][pieceX+1]==playerKR)and pieceY+2<8 and pieceX+2<8):
				board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY+1][pieceX+1]=0
				newPosY=pieceY+2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				turn=0
			if((board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX-1]==playeR)and pieceY-2>=0 and pieceX-2>=0):
				board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX-1]=0
				newPosY=pieceY-2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				turn=0
			if((board[pieceY-1][pieceX+1]==playerKR or board[pieceY-1][pieceX+1]==playeR)and pieceY-2>=0 and pieceX+2<8):
				board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX+1]=0
				newPosY=pieceY-2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				turn=0
	except:
		pass
	try:
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0 or board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0) and turn==1):
			move=input( 'Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playerB):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if((moveY==pieceY-1 or moveY==pieceY+1) and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board piece positions
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							printGrid()
							turn=0
						else:
							print('This move is not allowed')
				else:
					print('A piece is already there!')
			else:
				possibleMovesBKing()
	except:
		pass
#Controls the Black pieces moves
def possibleMovesB():
	global newPosX, newPosY,turn
	#Handles exception incase values are out of range
	try:
		#Checks if the chosen piece has a enemy's piece nearby
		if (board[pieceY-2][pieceX+2]==0 or board[pieceY-2][pieceX-2]==0):
			if((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)and pieceY-2>=0 and pieceX-2>=0):
				#Updates board
				board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX-1]=0
				#Stores piece's new coordinates
				newPosY=pieceY-2
				newPosX=pieceX-2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				doubleJumpB()
				printGrid()
				turn=0
			if((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR)and pieceY-2>=0 and pieceX+2<8):
				board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
				board[pieceY][pieceX]=0
				board[pieceY-1][pieceX+1]=0
				newPosY=pieceY-2
				newPosX=pieceX+2
				printGrid()
				print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
				#Checks if there's another immediate piece to be eaten and executes it 
				doubleJumpB()
				printGrid()
				turn=0
				
		elif(((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR) or (board[pieceY-1][pieceX-1]==playerKR or board[pieceY-1][pieceX+1]==playerKR)) and(board[pieceY+2][pieceX+2]!=0 and board[pieceY+2][pieceX-2]!=0)):
			print('...but there is not legal moves available. Try again :D')		
	except:
		pass
	try:
		#If there is no enemys pieces close to be eaten offers you to move said piece
		if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0) and turn==1):
			move=input( 'Where do you want it instead?' '\n')
			#Checks format, range, and correct piece chosen fullfil the game conditions
			if (len(move) == 3):
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playerB):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY-1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							#Updates board piece positions
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							printGrid()
							turn=0
						else:
							print('This move is not allowed')
				else:
					print('A piece is already there!')
			else:
				possibleMovesB()
	except:
		pass	
#Another jump will be taken if there's an enemy's piece to be eaten	
def doubleJumpB():
	if(board[newPosY][newPosX]==playerB):
		while(((board[newPosY-1][newPosX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)and board[newPosY-2][newPosX-2]==0) or ((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR) and (board[newPosY-2][newPosX+2]==0))):
			if(board[newPosY-1][newPosX-1]==playerR or board[pieceY-1][pieceX-1]==playerKR) and pieceY-1>=0 and pieceX-1>=0:
				input('Your enemy has a double jump available. Press enter to continue')
				#Updates board piece positions
				board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX-1]=0
				printGrid()
			elif(board[newPosY-1][newPosX+1]==playerR or board[pieceY-1][pieceX+1]==playerKR)and pieceY-1>=0 and pieceX+1<8:
				input('Your enemy has a double jump available. Press enter to continue')
				board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX+1]=0
				printGrid()
	#Checks if the piece to make the double jump is a King and allows them to make a double jump in any direction
	if(board[newPosY][newPosX]==playerKB):
		while(((board[newPosY+1][newPosX-1]==playeR or board[newPosY+1][newPosX-1]==playerKR) and board[newPosY+2][newPosX-2]==0) or((board[newPosY+1][newPosX+1]==playeR or board[newPosY+1][newPosX+1]==playerKR) and board[newPosY+2][newPosX+2]==0) or((board[newPosY-1][newPosX-1]==playeR or board[newPosY-1][newPosX-1]==playerKR)and board[newPosY-2][newPosX-2]==0) or ((board[newPosY-1][newPosX+1]==playeR or board[newPosY-1][newPosX+1]==playerKR) and board[newPosY-2][newPosX+2]==0)):
			if((board[newPosY+1][newPosX-1]==playeR or board[newPosY+1][newPosX-1]==playerKR) and pieceY+1<8 and pieceX-1>=0 ):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX-1]=0
				printGrid()
			if((board[newPosY+1][newPosX+1]==playeR or board[newPosY+1][newPosX+1]==playerKR) and pieceY+1<8 and pieceX+1<8 ):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY+1][newPosX+1]=0
				printGrid()
			if((board[newPosY-1][newPosX-1]==playeR or board[newPosY-1][newPosX-1]==playerKR) and pieceY-1>=0 and pieceX-1>=0):
				input('Another available piece to be eaten. Press enter to continue')
				# Updates board values
				board[newPosY-2][newPosX-2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX-1]=0
				printGrid()
			if((board[newPosY-1][newPosX+1]==playeR or board[newPosY-1][newPosX+1]==playerKR) and pieceY-1>=0 and pieceX+1<8):
				input('Another available piece to be eaten. Press enter to continue')
				board[newPosY-2][newPosX+2]=board[newPosY][newPosX]
				board[newPosY][newPosX]=0
				board[newPosY-1][newPosX+1]=0
				printGrid()
#Allows the user's on Two Player mode to undo or redo their moves
def undoRedo():
	global board, copyBoard,board2, turn
	undoBoard=input ('\n''Type undo if you would like to retake the turn. Otherwise press enter''\n')
	#If the input by the user is undo, the previous copy of the board before the move will be restored
	if(undoBoard=='undo' or undoBoard=='Undo'):
		#Restores the board copy before the move was made
		board=copyBoard[:]
		board=copy.deepcopy(copyBoard)
		printGrid()
		#Asks the user if they want to redo their previous move
		redoBoard=input('\n''Type redo if you would like to retake the turn. Otherwise press enter''\n')
		if(redoBoard=='redo' or redoBoard=='Redo'):
			#Restores the copy of the variable after the move was made(board2)
			board=board2[:]
			board=copy.deepcopy(board2)
			printGrid()
			#Changes the turn to the other player if the chose redo
			if(turn==1):
				turn=1
			elif(turn==0):
				turn=0
		# Checks if the user wants to make a different move after choosing undo
		elif(redoBoard!='redo' and turn==1):
			validateR()
		elif(redoBoard!='redo' and turn==0):
			validateB()
#Updates the board and pieces once they reache their opposite sides of the board to Kings
def CheckKing():
	#Using a for loop to check the first and last row and if they're in the opponents side
	for i in range(8):
		#If they have reach the end of the board, they will be converted to Kings
		if(board[7][i]==1):
		    board[7][i]=3
		    print('\n' 'WOW! Your piece is now a Red King' '\n')
		if(board[0][i]==2):
		    board[0][i]=4
		    print('\n' 'WOW! Your enemy has a Black King now' '\n')
#Determinates the winner of the game depending of whom has the last piece on the table
def checkVictory():
	#Creates to booleans to check the status of the board
	winnerR= False
	winnerB= False
	#Loops throught the whole board looking for pieces of both players
	for i in board:
		for j in i:
			if(j==playeR or j==playerKR):
				winnerR= True
			if(j==playerB or j==playerKB):
				winnerB=True
	#If one of the players doesn't have any pieces left, a winner will be declared
	if(winnerR == True and winnerB == False):
		print('\n''WOOHOO! RED PLAYER, YOU ARE A WINNER! ''\n')
		print('--------------GAME OVER--------------''\n')
		welcomeStart()
	if(winnerR == False and winnerB == True):
		print('\n''WOOHOO! RED PLAYER, YOU ARE A WINNER! ''\n')
		print('--------------GAME OVER--------------''\n')
		welcomeStart()
def validateAIR():
	#Assings a random number with the 0-7 range
	pieceY=(random.randint(0,7))
	pieceX=(random.randint(0,7))
	#Checks the values selected are correct
	if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
		#If a normal piece is selected, normal moves will be executed
		if(board[pieceY][pieceX]== playeR):
			try:
				#If there's a piece that can be eaten, it'll b executed first
				if(((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX-1]==playerKB)  and board[pieceY+2][pieceX-2]==0) or ((board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB) and board[pieceY+2][pieceX+2]==0)):
					#Makes user aware of the piece selected
					print('\n''Player 1 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					#Checks both sides for enemy's pieces that could be eaten
					if((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX-1]==playerKB)and pieceY+2<8 and pieceX-2>=0):
						#Updates board values
						board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY+1][pieceX-1]=0
						newPosY=pieceY+2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						#Checks if there's any double jumps available 
						doubleJumpR()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						#Changes turn to the other playerB
						global turn
						turn=1
					if((board[pieceY+1][pieceX+1]==playerB or board[pieceY+1][pieceX+1]==playerKB)and pieceY+2<8 and pieceX+2<8):
						board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY+1][pieceX+1]=0
						newPosY=pieceY+2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						doubleJumpR()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=1
				#If there's no nearby pieces to be eaten, it will move it to the next avalible square
				if((board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0) and turn==0):
					print('\n''Player 1 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY+1][pieceX-1]==0 and turn!=1 and pieceX-1>=0 and pieceY+1<8):
						board[pieceY+1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX-1)+', '+str(pieceY+1)+'\n')
						turn=1
					if(board[pieceY+1][pieceX+1]==0 and turn!=1 and pieceY+1<8 and pieceX+1<8):
						board[pieceY+1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX+1)+', '+str(pieceY+1)+'\n')
						turn=1
			except:
				pass
		#If the piece selected is a King, special will be unlocked
		if(board[pieceY][pieceX]== playerKR):
			try:
				#If there's a piece that can be eaten, it'll b executed first
				if (board[pieceY-2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY+2][pieceX+2]==0):
					if((board[pieceY-1][pieceX-1]==playerB or board[pieceY-1][pieceX-1]==playerKB)and pieceY-2>=0 and pieceX-2>=0):
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						doubleJumpR()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=1
					if((board[pieceY-1][pieceX+1]==playerB or board[pieceY-1][pieceX+1]==playerKB)and pieceY-2>=0 and pieceX+2<8):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						doubleJumpR()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=1
					if((board[pieceY+1][pieceX-1]==playerB or board[pieceY-1][pieceX-1]==playerKB)and pieceY+2<8 and pieceX-2>=0):
						board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceÝ+1][pieceX-1]=0
						newPosY=pieceY+2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						doubleJumpR()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=1
					if((board[pieceY+1][pieceX+1]==playerB or board[pieceY-1][pieceX+1]==playerKB)and pieceY+2<8 and pieceX+2<8):
						board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY+1][pieceX+1]=0
						newPosY=pieceY+2
						newPosX=pieceY+2
						printGrid()
						print('\n' 'Oh no! Player 1 ate one of your pieces!' '\n')
						doubleJumpR()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=1
			except:
				pass
			try:
				#If there's no Player 1's pieces neraby, it'll be moved to the next available spot
				if(board[pieceY-1][pieceX+1]==0 or board[pieceY-1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0 or board[pieceY+1][pieceX-1]==0):
					print('\n''Player 1 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==0 and turn!=1 and pieceY-1>=0 and pieceX+1<8):
						board[pieceY-1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=1
					if(board[pieceY-1][pieceX+1]==0 and turn!=1 and pieceY-1>=0 and pieceX+1<8):
						board[pieceY-1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=1
					if(board[pieceY+1][pieceX-1]==0 and turn!=1 and pieceY+1<8 and pieceX-1>=0):
						board[pieceY+1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX-1)+', '+str(pieceY+1)+'\n')
						turn=1
					if(board[pieceY+1][pieceX+1]==0 and turn!=1 and pieceY+1<8 and pieceX+1<8):
						board[pieceY+1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to '+str(pieceX+1)+', '+str(pieceY+1)+'\n')
						turn=1
			except:
				pass
def validateAIB():
	#Assings a random number with the 0-7 range
	pieceY=(random.randint(0,7))
	pieceX=(random.randint(0,7))
	#Checks the values selected are correct
	if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
		#If a normal piece is selected, normal moves will be executed
		if(board[pieceY][pieceX]== playerB):
			try:
				#If there's a piece that can be eaten, it'll b executed first
				if(((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)  and board[pieceY-2][pieceX-2]==0) or ((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR) and board[pieceY-2][pieceX+2]==0)):
					#Makes user aware of the piece selected
					print('\n''Player 2 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					#Checks both sides for Player 2's pieces that could be eaten
					if((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)and pieceY-2>=0 and pieceX-2>=0):
						#Updates board values
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						#Checks if there's any double jumps available 
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						#Changes turn to the other player
						global turn
						turn=0
					if((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR)and pieceY-2>=0 and pieceX+2<8):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
				#If there's no nearby pieces to be eaten, it will move it to the next avalible square
				if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0) and turn==1):
					print('\n''Player 2 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==0 and turn!=0 and pieceX-1>=0 and pieceY-1>=0):
						board[pieceY-1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY-1][pieceX+1]==0 and turn!=0 and pieceY-1>=0 and pieceX+1<8):
						board[pieceY-1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=0
			except:
				pass
		#If the piece selected is a King, special will be unlocked
		if(board[pieceY][pieceX]== playerKB):
			try:
				#If there's a piece that can be eaten, it'll b executed first
				if (board[pieceY-2][pieceX-2]==0 or board[pieceY-2][pieceX+2]==0 or board[pieceY+2][pieceX-2]==0 or board[pieceY+2][pieceX+2]==0):
					if((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)and pieceY-2>=0 and pieceX-2>=0):
						board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX-1]=0
						newPosY=pieceY-2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if((board[pieceY-1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR)and pieceY-2>=0 and pieceX+2<8):
						board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY-1][pieceX+1]=0
						newPosY=pieceY-2
						newPosX=pieceX+2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if((board[pieceY+1][pieceX-1]==playeR or board[pieceY-1][pieceX-1]==playerKR)and pieceY+2<8 and pieceX-2>=0):
						board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceÝ+1][pieceX-1]=0
						newPosY=pieceY+2
						newPosX=pieceX-2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
					if((board[pieceY+1][pieceX+1]==playeR or board[pieceY-1][pieceX+1]==playerKR)and pieceY+2<8 and pieceX+2<8):
						board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						board[pieceY+1][pieceX+1]=0
						newPosY=pieceY+2
						newPosX=pieceY+2
						printGrid()
						print('\n' 'Oh no! Player 2 ate one of your pieces!' '\n')
						doubleJumpB()
						printGrid()
						print('\n''And moved it to: '+str(newPosX)+', '+str(newPosY)+'\n')
						turn=0
			except:
				pass
			try:
				#If there's no Player 2's pieces neraby, it'll be moved to the next available spot
				if(board[pieceY-1][pieceX+1]==0 or board[pieceY-1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0 or board[pieceY+1][pieceX-1]==0):
					print('\n''Player 2 has chosen: '+str(pieceX)+', '+str(pieceY)+'\n')
					if(board[pieceY-1][pieceX-1]==0 and turn!=0 and pieceY-1>=0 and pieceX+1<8):
						board[pieceY-1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX-1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY-1][pieceX+1]==0 and turn!=0 and pieceY-1>=0 and pieceX+1<8):
						board[pieceY-1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX+1)+', '+str(pieceY-1)+'\n')
						turn=0
					if(board[pieceY+1][pieceX-1]==0 and turn!=0 and pieceY+1<8 and pieceX-1>=0):
						board[pieceY+1][pieceX-1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX-1)+', '+str(pieceY+1)+'\n')
						turn=0
					if(board[pieceY+1][pieceX+1]==0 and turn!=0 and pieceY+1<8 and pieceX+1<8):
						board[pieceY+1][pieceX+1]=board[pieceY][pieceX]
						board[pieceY][pieceX]=0
						printGrid()
						print('\n''And moved it to: '+str(pieceX+1)+', '+str(pieceY+1)+'\n')
						turn=0
			except:
				pass
#Contains the main menu and controls the game
def welcomeStart():
	input('Welcome to checkers! Press enter to start')
	gameMode=input('\n''ARCADE MODE: Press 1 │ TWO PLAYER: Press 2 │ AI vs AI: Press 3 │ HELP: Press 4 │ QUIT: exit''\n')
	#Lets user now who is staring the game
	print('\n' 'You are playing as Rs')
	printGrid()
	#Selects a game mode
	if(gameMode=='1'):
		while(True):
			try:	
				#Controls turns against the computer
				arcadeMode()
			except ValueError:
				print('Incorrect input')
	if(gameMode=='2'):
		while(True):
			try:
				#Controls turns between player
				twoPlayerMode()
			except ValueError:
				print('Incorrect input')
	if(gameMode=='3'):
		while(True):
			try:
				#Controls turns between computer vs computer
				aiVSaiMode()
			except ValueError:
				print('Incorrect input')
	if (gameMode=='4'):
		print('\n''The aim of this game is to take every enemys piece by jumping over them. If your piece is in front of your opponents and it is your turn, theirs will be taken.''\n')
		print('\n''Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3 2)''\n')
		print('\n' '----------------------GOOD LUCK!--------------------' '\n')
		#Goes back to the game after instructions have been provaided
		welcomeStart()
	if(gameMode=='exit'):
		sys.exit()
	else:
		welcomeStart()
#starts the game
welcomeStart()
sys.exit()
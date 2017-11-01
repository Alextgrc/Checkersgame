import random
import sys
board = [[0, 1, 0, 0, 0, 1, 0, 1],
 		  [1, 0, 2, 0, 1, 0, 1, 0],
 		  [0, 0, 0, 1, 0, 0, 0, 0],
 		  [0, 0, 1, 0, 0, 0, 0, 0],
 		  [0, 2, 0, 0, 0, 1, 0, 0],
 		  [0, 0, 2, 0, 2, 0, 0, 0],
 		  [0, 2, 0, 2, 0, 2, 0, 1],
 		  [2, 0, 0, 0, 2, 0, 0, 0]]
#board = [[0, 1, 0, 1, 0, 1, 0, 1],
# 		  [1, 0, 1, 0, 1, 0, 1, 0],
#		  [0, 1, 0, 1, 0, 1, 0, 1],
# 		  [0, 0, 0, 0, 0, 0, 0, 0],
 #		  [0, 0, 0, 0, 0, 0, 0, 0],
 #		  [2, 0, 2, 0, 2, 0, 2, 0],
# 		  [0, 2, 0, 2, 0, 2, 0, 2],
# 		  [2, 0, 2, 0, 2, 0, 2, 0]]
board_size=8  
y=0
playeR= 1
playerB=2
turn=0
#Converts numbers into characters
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

#Prints the grid
def printGrid():
	CheckKing()
	print(' 0 1 2 3 4 5 6 7')
	print('┌─┬─┬─┬─┬─┬─┬─┬─┐')
	#Loops through the grid printing it
	for y in range(board_size):
		print('│' + intToText(board[y][0]) + '│' + intToText(board[y][1]) + '│' + intToText(board[y][2]) + '│' + intToText(board[y][3]) + '│' + intToText(board[y][4]) + '│' + intToText(board[y][5]) + '│' + intToText(board[y][6]) + '│' + intToText(board[y][7]) + '│' '\n'
	      '├─┼─┼─┼─┼─┼─┼─┼─┤')

	print('└─┴─┴─┴─┴─┴─┴─┴─┘')

#Controls turns checking if turn varible state has changed to the other player
def playerTurn():
	if(turn==0):
		validateR()

	if (turn==1):
		validateB()
#Executes player R moves		
def validateR():
		global piece, pieceX, pieceY, move, moveX, moveY
		piece = input('\n' 'It is player Rs turn. Choose your piece to move:' '\n')
		if ( piece == 'help'):
		    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3 2)')
		    print('')
		#Checks if the input is on the correct format
		if (len(piece) == 3):
			splitcord= piece.split(',')
			pieceX=int(splitcord[0])
			pieceY=int(splitcord[1])
			if(pieceX <8 and pieceX >=0 and pieceY <8 and pieceY >=0 ):	
				#Checks if a players piece is there to be moved
				if(board[pieceY][pieceX]== playeR):
					print('\n' 'Right piece!' '\n')
					#Checks if there's an enemy's piece there to be eaten and handles the exception for columns 0 and 7
					possibleMovesR()
				else:
					print('Cannot move this piece. Try again :)')

		else:
			print('Invalid input. Type \'help\' if you\'re stuck')
def possibleMovesR():
	global newPosX, newPosY
	try:
		
		if((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB) and(board[pieceY+2][pieceX+2]!=playerB or board[pieceY+2][pieceX-2]!=playerB)):
			eat=input('\n' 'Available piece to be eaten.Press Y to eat or N not to' '\n')					
			#Moves the piece chosen over the enemy's piece and eats it
			if(eat=='Y' or eat=='y'):
				if(board[pieceY+1][pieceX-1]==playerB):
					board[pieceY+2][pieceX-2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY+1][pieceX-1]=0
					newPosY=pieceY+2
					newPosX=pieceX-2
					
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					global turn
					print(newPosX, newPosY)
					doubleJumpR()
					printGrid()
					turn=1
					
				elif(board[pieceY+1][pieceX+1]==playerB):
					board[pieceY+2][pieceX+2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY+1][pieceX+1]=0
					newPosY=pieceY+2
					newPosX=pieceX+2
					
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					print(newPosX, newPosY)
					doubleJumpR()
					printGrid()
					turn=1
					
			#Asks where do you want to move it instead
			if(eat=='N' or eat=='n'):
				move=input('\n' 'Where do you want it instead?' '\n')
				#Checks it's the right input format
				if (len(move) == 3):
					splitcord= move.split(',')
					moveX=int(splitcord[0])
					moveY=int(splitcord[1])
					if(board[moveY][moveX]!=playeR):
						if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
							if(moveY==pieceY+1 and (moveX== pieceX+1 or moveX== pieceX-1)):
								board[moveY][moveX]=board[pieceY][pieceX]
								board[pieceY][pieceX]=0
								printGrid()
								turn=1
								
							else:
								print('This move is not allowed')

					else:
						print('A piece is already there!')
		elif((board[pieceY+1][pieceX-1]==playerB or board[pieceY+1][pieceX+1]==playerB) and(board[pieceY+2][pieceX+2]==playerB or board[pieceY+2][pieceX-2]==playerB)):
			print('...but there is not legal moves available. Try again :D')
	except:
		pass
	try:	
		if((board[pieceY+1][pieceX-1]==0 or board[pieceY+1][pieceX+1]==0)and turn!=1): 
			move=input('Where do you want it instead?' '\n')

			if (len(move) == 3):
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playeR):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY+1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							printGrid()
							turn=1
						else:
							print('This move is not allowed')

				else:
					print('A piece is already there!')
	except:
		pass
def doubleJumpR():
	if((board[newPosY+1][newPosX-1]==playerB) and(board[newPosY+2][newPosX+2]!=playerB or board[newPosY+2][newPosX-2]!=playerB)):
		input('Another available piece to be eaten. Press enter to continue')
		board[newPosY+2][newPosX-2]=board[newPosY][newPosX]
		board[newPosY][newPosX]=0
		board[newPosY+1][newPosX-1]=0
	elif((board[newPosY+1][newPosX+1]==playerB) and(board[newPosY+2][newPosX+2]!=playerB or board[newPosY+2][newPosX-2]!=playerB)):
		input('Another available piece to be eaten. Press enter to continue')
		board[newPosY+2][newPosX+2]=board[newPosY][newPosX]
		board[newPosY][newPosX]=0
		board[newPosY+1][newPosX+1]=0
def validateB():
		piece = input('\n' 'Its player B turn! Choose your piece to move:' '\n')
		if ( piece == 'help'):
		    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3 2)')
		    print('')		    
		if (len(piece) == 3):
			splitcord= piece.split(',')
			pieceX=int(splitcord[0])
			pieceY=int(splitcord[1])
			if(pieceX >=0 and pieceX <8 and pieceY >=0 and pieceY <8):
				if(board[pieceY][pieceX]== playerB):
					print('\n''Right piece!''\n')
					possibleMovesB()
				else:
					print('Cannot move this piece. Try again :)')
				
		else:
			print('Invalid input. Type \'help\' if you\'re stuck')
def possibleMovesB():
	try:
		if((board[pieceY-1][pieceX-1]==playeR or board[pieceY-1][pieceX+1]==playeR) and (board[pieceY-2][pieceX+2]!=playeR or board[pieceY-2][pieceX-2]!=playeR)):
			eat=input('\n' 'Available piece to be eaten.Press Y to eat or N not to' '\n')					
			if(eat=='Y' or eat=='y'):
				if(board[pieceY-1][pieceX-1]==playeR):
					board[pieceY-2][pieceX-2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY-1][pieceX-1]=0
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					global turn
					turn=0
				elif(board[pieceY-1][pieceX+1]==playeR):
					board[pieceY-2][pieceX+2]=board[pieceY][pieceX]
					board[pieceY][pieceX]=0
					board[pieceY-1][pieceX+1]=0
					printGrid()
					print('\n' 'CONGRATS! You ate an enemy piece!' '\n')
					turn=0
			elif(eat=='N' or eat=='n'):
				move=input('\n' 'Where do you want it?' '\n')
				if (len(move) == 3):
					splitcord= move.split(',')
					moveX=int(splitcord[0])
					moveY=int(splitcord[1])
					if(board[moveY][moveX]!=playerB):
						if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
							if(moveY==pieceY-1 and (moveX== pieceX+1 or moveX== pieceX-1)):
								board[moveY][moveX]=board[pieceY][pieceX]
								board[pieceY][pieceX]=0
								printGrid()
								turn=0
							else:
								print('This move is not allowed')
					else:
						print('A piece is already there!')
	except:
		pass
	try:
		if((board[pieceY-1][pieceX-1]==0 or board[pieceY-1][pieceX+1]==0) and turn!=0):
			move=input( 'Where do you want it?' '\n')

			if (len(move) == 3):
				splitcord= move.split(',')
				moveX=int(splitcord[0])
				moveY=int(splitcord[1])
				if(board[moveY][moveX]!=playerB):
					if(moveX >=0 and moveX <8 and moveY >=0 and moveY <8):
						if(moveY==pieceY-1 and (moveX== pieceX+1 or moveX== pieceX-1)):
							board[moveY][moveX]=board[pieceY][pieceX]
							board[pieceY][pieceX]=0
							printGrid()
							turn=0
						else:
							print('This move is not allowed')
				else:
					print('A piece is already there!')
	except:
		pass	

def CheckKing():
	for i in range(8):
		if(board[7][i]==1):
		    board[7][i]=3
		    print('\n' 'WOW! Your piece is now a Red King' '\n')
		if(board[0][i]==2):
		    board[0][i]=4
		    print('\n' 'WOW! Your piece is now a Black King' '\n')

input('Welcome to checkers! Press enter to start')
print('\n' 'You are playing as Rs')
printGrid()
while(True):
	try:	
		playerTurn()
	except ValueError:
		print('Incorrect input')


sys.exit

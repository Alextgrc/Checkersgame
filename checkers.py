import random
import sys
board = [[0, 1, 0, 1, 0, 1, 0, 1],
 		  [1, 0, 1, 0, 1, 0, 1, 0],
 		  [0, 1, 0, 1, 0, 1, 0, 1],
 		  [0, 0, 0, 0, 0, 0, 0, 0],
 		  [0, 0, 0, 0, 0, 0, 0, 0],
 		  [2, 0, 2, 0, 2, 0, 2, 0],
 		  [0, 2, 0, 2, 0, 2, 0, 2],
 		  [2, 0, 2, 0, 2, 0, 2, 0]]
board_size=8  
y=0
playeR= 1
#Converts numbers into characters
def intToText(num):
	if(num == 0): 
		return ' '
	if(num == 1): 
		return 'R'
	if(num == 2): 
		return 'B'

#Prints the grid
def printGrid():
	print('┌─┬─┬─┬─┬─┬─┬─┬─┐')
	for y in range(board_size):
		print('│' + intToText(board[y][0]) + '│' + intToText(board[y][1]) + '│' + intToText(board[y][2]) + '│' + intToText(board[y][3]) + '│' + intToText(board[y][4]) + '│' + intToText(board[y][5]) + '│' + intToText(board[y][6]) + '│' + intToText(board[y][7]) + '│' '\n'
	      '├─┼─┼─┼─┼─┼─┼─┼─┤')
	print('└─┴─┴─┴─┴─┴─┴─┴─┘')
def movePiece():
	while(True):
		move = input('\n' 'Your turn. Choose your piece to move:' '\n')
		if ( move == 'help'):
		    print('Type the coordinates (originating from the top left) of the box you want to put a cross into in the format \'y,x\' (e.g. 3 2)')
		    print('')
		    continue

		if (len(move) == 3):
			splitcord= move.split(',')
			cordX=int(splitcord[0])
			cordY=int(splitcord[1])
			if(cordX >=0 and cordX <=7 and cordY >=0 and cordY <=7):
				if(board[cordY][cordX]== playeR):
					print('right piece!')
					move=input('\n' 'Where do you want it?' '\n')

					if(board[cordY+1][cordX+1]==0):
						board[cordY +1][cordX+1]=board[cordY][cordX]
						board[cordY][cordX]=0
						printGrid()
					
				else:
					print('cannot move this bish')

		else:
			print('Invalid input. Type \'help\' if you\'re stuck')

input('Welcome to checkers! Press enter to start')
print('\n' 'You are playing as Rs')
printGrid()
movePiece()



sys.exit
import pygame
import random
import numpy as np

pygame.init()

display_width = 800
display_height = 600

board_width = 210
board_height = 160

## For testing purposes
np.set_printoptions(threshold='nan', linewidth='nan')

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Amidar')
clock = pygame.time.Clock()

item_width = 10

itemImg = pygame.image.load('item.png')
opponentImg = pygame.image.load('opponent.png')

class Board():

    def __init__(self, board=None):
        if board is None:
            self.board = self.create_board()
        else:
            self.board = board

    def create_board(self):
        self.board = [[0 for x in range(board_width)] for y in range(board_height)]

        ##  Rows
        for i in range(board_width):
            self.board[0][i] = 1
            self.board[31][i] = 1
            self.board[63][i] = 1
            self.board[95][i] = 1
            self.board[127][i] = 1
            self.board[board_height-1][i] = 1

        ## Outside border
        for i in range(board_height):
            self.board[i][0] = 1
            self.board[i][board_width-1] = 1

        ## First row columns
        first_row = [50, 65, 90, 110, 145, 160]
        for i in range(0, 32):
            for j in first_row:
                self.board[i][j] = 1

        second_row = [35, 60, 75, 120, 135, 175]
        for i in range(32, 64):
            for j in second_row:
                self.board[i][j] = 1

        third_row = [30, 80, 130, 180] 
        for i in range(64, 96):
            for j in third_row:
                self.board[i][j] = 1

        fourth_row = [40, 105, 115, 170]
        for i in range(96, 128):
            for j in fourth_row:
                self.board[i][j] = 1

        fifth_row = [41, 83, 125, 167]
        for i in range(128, 160):
            for j in fifth_row:
                self.board[i][j] = 1

        print(np.matrix(self.board))
        

def opponents(opponentx, opponenty, opponentw, opponenth):
	gameDisplay.blit(opponentImg, (opponentx, opponenty))

def item(x, y):
	gameDisplay.blit(itemImg, (x, y))

def text_objects(text, font):
	textSurface = font.render(text, True, blue)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(TextSurf, TextRect)

	time.sleep(2)

	game_loop()

def crash():
	message_display('Out of bound')

def game_loop():
	x = (display_width * 0.45)
	y = (display_height * 0.8)

	opponentx = random.randrange(0, display_width)
	opponenty = random.randrange(0, display_height)
	opponenth = 10
	opponentw = 10

	gameEnd = False
	x_change = 0
	y_change = 0


	while not gameEnd:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameEnd = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -3
				elif event.key == pygame.K_RIGHT:
					x_change = 3
				elif event.key == pygame.K_UP:
					y_change = -3
				elif event.key == pygame.K_DOWN:
					y_change = 3

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
					x_change = 0
					y_change = 0

		x += x_change
		y += y_change
		opponents(opponentx, opponenty, opponentw, opponenth)
		#opponenty += 7
		item(x, y)

		if x > display_width - item_width or x < 0:
			crash()

		if y < opponenty + opponenth:
			print('crash')

			if x > opponentx and x < opponentx + opponentw or x + item_width > opponentx and x + item_width < opponentx + opponentw:
				print('full crash')
				crash()

		pygame.display.update()
		clock.tick(60)
Board()
game_loop()
pygame.quit()
quit()

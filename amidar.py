import pygame
import random
import numpy as np
import abc

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


class Actor():
    __metaclass__ = abc.ABCMeta

    def __init__(self, x=None, y=None):
        '''Can create one at a given spot or a 'random' spot?'''
        if x is not None:
            self.x = x
        else:
            self.x = 0
        if y is not None:
            self.y = y
        else:
            self.y = 0

    def get_moves(self, board):
        ''' returns list of moves in the form of: "left up down right" '''
        moves = []
        x = self.x
        y = self.y

        print board.board[x-1][y]
        print board.board[x+1][y]
        print board.board[x][y-1]
        print board.board[x][y+1]
        if board.board[x-1][y] is not None and board.board[x-1][y] != 0:
            moves.append("left")
        if board.board[x+1][y] is not None and board.board[x+1][y] != 0:
            moves.append("right")
        if board.board[x][y-1] is not None and board.board[x][y-1] != 0:
            moves.append("down")
        if board.board[x][y+1] is not None and board.board[x][y+1] != 0:
            moves.append("up")

        return moves

    @abc.abstractmethod
    def make_move(self, board, move):
        ''' make a move given a board and a move '''
        pass

    @abc.abstractmethod
    def draw(self):
        ''' draw the actor on the board '''
        pass

    @abc.abstractproperty
    def speed(self):
        pass

class Player(Actor):
    speed = 1

    def make_move(self, board, move):
        if move in self.get_moves(board): 
            print move
            if move == 'right':
                self.x += self.speed
            if move == 'down':
                self.y += self.speed
            if move == 'left':
                self.x -= self.speed
            if move == 'up':
                self.y -= self.speed

    def draw(self):
        gameDisplay.blit(itemImg, (self.x, self.y))


class Opponent(Actor):

    speed = 1
    direction = None

    def make_move(self, board, move):
        ''' Follow all the logic of the opponent '''
        self.direction = "left"
        self.x += self.speed

    def draw(self):
        gameDisplay.blit(opponentImg, (self.x, self.y))


class Board():

    def __init__(self, board=None):
        if board is None:
            self.board, self.paths = self.create_board()
        else:
            self.board = board

    ## WE NEED TO ROTATE THE BOARD...
    def create_board(self):
        self.board = [[0 for x in range(board_width)] for y in range(board_height)]

        ##  Rows
        for i in range(board_width):
            self.board[0][i] = Path(0, i)
            self.board[31][i] = Path(31, i)
            self.board[63][i] = Path(63, i)
            self.board[95][i] = Path(95, i)
            self.board[127][i] = Path(127, i)
            self.board[board_height-1][i] = Path(board_height-1, i)

        ## Outside border
        for i in range(board_height):
            self.board[i][0] = Path(i, 0)
            self.board[i][board_width-1] = Path(i, board_width-1)

        ## First row columns
        first_row = [50, 65, 90, 110, 145, 160]
        for i in range(0, 32):
            for j in first_row:
                self.board[i][j] = Path(i, j)

        second_row = [35, 60, 75, 120, 135, 175]
        for i in range(32, 64):
            for j in second_row:
                self.board[i][j] = Path(i, j)

        third_row = [30, 80, 130, 180] 
        for i in range(64, 96):
            for j in third_row:
                self.board[i][j] = Path(i, j)

        fourth_row = [40, 105, 115, 170]
        for i in range(96, 128):
            for j in fourth_row:
                self.board[i][j] = Path(i, j)

        fifth_row = [41, 83, 125, 167]
        for i in range(128, 160):
            for j in fifth_row:
                self.board[i][j] = Path(i, j)

        paths = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if isinstance(self.board[i][j], Path):
                    paths.append(self.board[i][j])

        # print(np.matrix(self.board))
        return self.board, paths

class Path():
    def __init__(self, y, x):
        self.passed = False
        self.contains = None
        self.x = x
        self.y = y

    def moved(self, thing):
        self.contains = thing
        if type(thing) is Player:
            self.passed = True

    def moved_off(self):
        self.contains = None

    def draw(self):
        pygame.draw.rect(gameDisplay, (0,0,255), (self.x, self.y, 10, 10))


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
    x = int(0)
    y = int(0)
    player = Player(x, y)
    board = Board()

    opponentx = random.randrange(0, display_width)
    opponenty = random.randrange(0, display_height)
    opponenth = 10
    opponentw = 10

    opponent = Opponent(opponentx, opponenty)

    gameEnd = False
    x_change = 0
    y_change = 0

    while not gameEnd:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameEnd = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.make_move(board, "left")
                    ##x_change = -3
                elif event.key == pygame.K_RIGHT:
                    player.make_move(board, "right")
                    ##x_change = 3
                elif event.key == pygame.K_UP:
                    player.make_move(board, "up")
                    ##y_change = -3
                elif event.key == pygame.K_DOWN:
                    player.make_move(board, "down")
                    ##y_change = 3
                opponent.make_move(board, "right")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        x_change = 0
                        y_change = 0

        for path in board.paths:
            path.draw()
        opponent.draw()
        player.draw()
        #opponenty += 7


        if x > display_width - item_width or x < 0:
            crash()

        '''if y < opponenty + opponenth:
            print('crash')
        '''
        if x > opponentx and x < opponentx + opponentw or x + item_width > opponentx and x + item_width < opponentx + opponentw:
            print('full crash')
            crash()

        pygame.display.update()
        clock.tick(60)
game_loop()
pygame.quit()
quit()

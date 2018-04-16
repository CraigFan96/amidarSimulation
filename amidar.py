import pygame
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Amidar')
clock = pygame.time.Clock()

item_width = 10

itemImg = pygame.image.load('item.png')
opponentImg = pygame.image.load('opponent.png')

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

game_loop()
pygame.quit()
quit()
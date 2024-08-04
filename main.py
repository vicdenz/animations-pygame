import pygame
from random import randint
from square import Square
from gradients import diagonal_gradient

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
SPAWN_SQUARE = pygame.USEREVENT + 1

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Animations")

clock = pygame.time.Clock()

rects = []
rect_color = (255, 150, 69, 40)

bg_color1 = (255, 174, 69)
bg_color2 = (103, 63, 105)

gradient_surface = diagonal_gradient(WIDTH, HEIGHT, bg_color1, bg_color2)

pygame.time.set_timer(SPAWN_SQUARE, randint(750, 1500))

running = True
while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.KMOD_LCTRL:
				running = False
			
			if event.key == pygame.KMOD_SPACE:
				rects.append(Square(rect_color, WIDTH, HEIGHT))
		
		if event.type == SPAWN_SQUARE:
			rects.append(Square(rect_color, WIDTH, HEIGHT))
			pygame.time.set_timer(SPAWN_SQUARE, randint(1000, 2000))

	screen.blit(gradient_surface, [0,0])

	r = 0
	while (r < len(rects)):
		rects[r].draw(screen)
		
		if rects[r].update(HEIGHT):
			rects.pop(r)
		else:
			r += 1

	pygame.display.flip()

pygame.quit()
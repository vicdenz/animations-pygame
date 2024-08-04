import pygame

def diagonal_gradient(width, height, color1, color2):
	gradient = pygame.Surface((width, height))
	for x in range(width):
		for y in range(height):
			t = (x + y) / (width + height)
			r = (1 - t) * color1[0] + t * color2[0]
			g = (1 - t) * color1[1] + t * color2[1]
			b = (1 - t) * color1[2] + t * color2[2]
			gradient.set_at((x, y), (int(r), int(g), int(b)))
	return gradient

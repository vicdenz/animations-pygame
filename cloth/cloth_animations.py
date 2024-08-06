import pygame
import time
import numpy as np
from random import randint

from point import Point
from edge import Edge

clock = pygame.time.Clock()
pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cloth Animations")

points = []
edges = []
n = 10
offset = 100
dist = 20
point_radius = 4
edge_width = 1

for row in range(n):
	for col in range(n):
		points.append(Point(offset+col*dist, offset+row*dist, point_radius, (50, 50, 50), acc=np.array([0, 1], dtype=float)))
points[0].fixed = True
points[n-1].fixed = True

for row in range(n):
	for col in range(n):
		if col < n-1:
			edges.append(Edge(points[row*n+col], points[row*n+col+1], edge_width, (20, 20, 20)))
		if row < n-1:
			edges.append(Edge(points[row*n+col], points[(row+1)*n+col], edge_width, (20, 20, 20)))

def draw_screen(screen):
	screen.fill((255, 255, 255))

	for point in points:
		point.draw(screen)

	for edge in edges:
		edge.draw(screen)

	pygame.display.flip()

last_time = time.time()
FPS = 24
running = True
while running:
	dt = (time.time() - last_time) * FPS
	last_time = time.time()
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LCTRL:
				running = False

		if event.type == pygame.MOUSEMOTION:
			points[n-1].set_pos(event.pos[0], event.pos[1])

	# move
	for point in points:
		point.update(dt)

	for edge in edges:
		edge.check_dist()

	# draw
	draw_screen(screen)

pygame.quit()
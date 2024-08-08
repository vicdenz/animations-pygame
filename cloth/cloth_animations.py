import pygame
import numpy as np
import time, json
from random import randint

from point import Point
from edge import Edge

clock = pygame.time.Clock()
pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cloth Animations")

color = (200, 70, 20)
gravity = np.array([0, 1], dtype=float)

def load_cloth(path):
	cloth_data = json.load(open(path, 'r'))
	offset = cloth_data['offset']
	scale = cloth_data['scale']

	points = []
	for point in cloth_data['points']:
		points.append(Point(offset+point[0]*scale, offset+point[1]*scale, color, acc=gravity))

	edges = []
	for edge in cloth_data['edges']:
		edges.append(Edge(points[edge[0]], points[edge[1]], color))

	for p in cloth_data['fixed']:
		points[p].fixed = True
	
	return points, edges, scale

points, edges, scale = load_cloth("rag.json")

cloth = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

def draw_screen(screen):
	screen.fill((255, 255, 255))

	if render_cloth:
		cloth.fill((0, 0, 0, 0))

		for edge in edges:
			edge.draw(cloth)

		cloth_mask = pygame.mask.from_surface(cloth)
		cloth_outline = cloth_mask.outline()

		if len(cloth_outline) > 2:
			pygame.draw.polygon(screen, color, cloth_outline)
	else:
		for edge in edges:
			edge.draw(screen)

	pygame.display.flip()

render_cloth = False
last_time = time.time()
FPS = 60
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
			
			if event.key == pygame.K_r:
				render_cloth = not render_cloth

		if event.type == pygame.MOUSEMOTION:
			points[0].set_pos(event.pos[0]-scale*5, event.pos[1])
			points[9].set_pos(event.pos[0]+scale*5, event.pos[1])

	# move
	for point in points:
		point.update(dt)

	for edge in edges:
		edge.check_dist()

	# draw
	draw_screen(screen)

pygame.quit()
import pygame
import time
import numpy as np
from particle import Particle
from random import randint

clock = pygame.time.Clock()
pygame.init()

WIDTH, HEIGHT = 600, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Orbits Animations")

font = pygame.font.SysFont(None, 24)

particles = []
n = 5

def new_particles():
	global particles, n

	particles = []
	for i in range(n):
		mass = randint(1, 1)
		particles.append(Particle(randint(10, WIDTH-10), randint(10, HEIGHT-10), mass, mass*10, (randint(50, 200), randint(50, 200), randint(50, 200))))
		particles[i].set_vel(np.array([randint(-5, 5), randint(-5, 5)], dtype=float))

sqrt3_by_2 = 0.86602540378
particles = [
	Particle(300, 300, 1, 10, (155, 20, 20)),
	Particle(200, 300+100*sqrt3_by_2, 1, 10, (20, 155, 20)),
	Particle(400, 300+100*sqrt3_by_2, 1, 10, (20, 20, 155)),
]
path = []
# new_particles()

last_time = time.time()
FPS = 120
running = True
while running:
	dt = (time.time() - last_time) * FPS
	last_time = time.time()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LCTRL:
				running = False
			
			if event.key == pygame.K_SPACE:
				new_particles()
				path = []

	for i in range(len(particles)):
		net_force = np.zeros(2, dtype=float)
		particle = particles[i]
		for j in range(len(particles)):
			if i != j:
				net_force += particle.calculate_grav_force(particles[j])
		particle.apply_force(net_force)

	screen.fill((255, 255, 255))

	for p in range(len(path)):
		if p < len(path)-len(particles)-1:
			pygame.draw.aaline(screen, path[p][1], path[p][0], path[p+len(particles)][0], 1)

	for particle in particles:
		particle.update(dt)
		path.append([particle.pos, particle.color])
		particle.draw(screen)

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
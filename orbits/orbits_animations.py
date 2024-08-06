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
		mass = randint(1, 5)
		particles.append(Particle(randint(10, WIDTH-10), randint(10, HEIGHT-10), mass, mass*5, (i*(255//n), i*(255//n), i*(255//n))))
		particles[i].set_vel(np.array([randint(-5, 5), randint(-5, 5)], dtype=float))

new_particles()

last_time = time.time()
FPS = 60
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

	for i in range(len(particles)):
		net_force = np.zeros(2, dtype=float)
		particle = particles[i]
		for j in range(len(particles)):
			if i != j:
				net_force += particle.calculate_grav_force(particles[j])
		print(net_force, i)
		particle.apply_force(net_force)

	screen.fill((255, 255, 255))

	for particle in particles:
		particle.update(dt)
		particle.draw(screen)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()
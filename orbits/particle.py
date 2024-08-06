import pygame
import numpy as np

class Particle:
	G = 2000

	def __init__(self, x, y, mass, radius, color):
		self.pos = np.array([x, y], dtype=float)
		self.last_pos = self.pos

		self.acc = np.zeros(2, dtype=float)

		self.mass = mass

		self.radius = radius
		self.color = color

	def calculate_grav_force(self, p2):
		dist = p2.pos - self.pos
		r = np.linalg.norm(dist)
		if r == 0:
			return np.zeros(2, dtype=float)

		g_force = self.G * self.mass * p2.mass / r**2
		return g_force * dist / r

	def set_vel(self, vel):
		self.last_pos = self.pos - vel

	def apply_force(self, force):
		self.acc = force / self.mass

	# https://youtu.be/qEp70jK8Az0?t=428
	def update(self, dt):
		new_pos = 2 * self.pos - self.last_pos + dt**2 * self.acc
		self.last_pos = self.pos
		self.pos = new_pos
	
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.pos, self.radius)
import pygame
import numpy as np

class Point:
	def __init__(self, x, y, radius, color, fixed=False, acc=np.zeros(2, dtype=float)):
		self.pos = np.array([x, y], dtype=float)
		self.last_pos = self.pos

		self.fixed = fixed
		self.acc = acc

		self.radius = radius
		self.color = color
	
	def set_pos(self, x, y):
		self.pos[0] = x
		self.pos[1] = y
		self.last_pos = self.pos

	# https://youtu.be/qEp70jK8Az0?t=428
	def update(self, dt):
		if not self.fixed:
			new_pos = 2 * self.pos - self.last_pos + dt**2 * self.acc
			self.last_pos = self.pos
			self.pos = new_pos
	
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.pos.astype(int), self.radius)
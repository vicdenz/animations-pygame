import pygame
import numpy as np

class Edge:
	elasticity = 0.8

	def __init__(self, p1, p2, color, width=2):
		self.p1 = p1
		self.p2 = p2

		self.max_length = np.linalg.norm(self.p2.pos - self.p1.pos)

		self.width = width
		self.color = color

	def check_dist(self):
		current_dist = self.p2.pos - self.p1.pos
		current_length = np.linalg.norm(current_dist)

		if current_length > self.max_length:
			unit_dist = current_dist / current_length

			if self.p1.fixed:
				self.p2.pos = self.p1.pos + unit_dist * self.max_length * self.elasticity
			elif self.p2.fixed:
				self.p1.pos = self.p2.pos - unit_dist * self.max_length * self.elasticity
			else:
				midpoint = (self.p1.pos + self.p2.pos) / 2
				self.p1.pos = midpoint - unit_dist * self.max_length / 2 * (2 - self.elasticity)
				self.p2.pos = midpoint + unit_dist * self.max_length / 2 * (2 - self.elasticity)

	def draw(self, screen):
		pygame.draw.line(screen, self.color, self.p1.pos, self.p2.pos, self.width)
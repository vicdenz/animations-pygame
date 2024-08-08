import pygame
import numpy as np

class Edge:
	def __init__(self, p1, p2, color, width=2, elasticity=1):
		self.p1 = p1
		self.p2 = p2

		self.max_length = np.linalg.norm(self.p2.pos - self.p1.pos)

		self.width = width
		self.color = color

		self.elasticity = elasticity

	def check_dist(self):
		current_dist = self.p2.pos - self.p1.pos
		current_length = np.linalg.norm(current_dist)
		unit_dist = current_dist / current_length

		dist_diff = current_length - self.max_length

		if self.p1.fixed:
			self.p2.pos -= dist_diff * unit_dist * self.elasticity
		elif self.p2.fixed:
			self.p1.pos += dist_diff * unit_dist * self.elasticity
		else:
			self.p1.pos += dist_diff * unit_dist / 2 * self.elasticity
			self.p2.pos -= dist_diff * unit_dist / 2 * self.elasticity

	def draw(self, screen):
		pygame.draw.line(screen, self.color, self.p1.pos, self.p2.pos, self.width)
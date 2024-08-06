import pygame
from random import randint

class Square:
	def __init__(self, color, width, height):
		self.create(color, width, height)

	def create(self, color, width, height):
		self.size = randint(50, 100)

		self.x = randint(self.size//2, width-self.size//2)
		self.y = height+self.size//2

		self.vel_x = 0
		self.vel_y = -randint(1, 2)

		self.deg = 0
		self.rot_speed = (2*randint(0,1)-1)*randint(1,2)

		self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		# pygame.draw.rect(self.surf, [ch+randint(-10, 10) for ch in color], [0, 0, self.size, self.size])
		pygame.draw.rect(self.surf, color, [0, 0, self.size, self.size])
	
	def update(self, height):
		# falling
		self.x += self.vel_x
		self.y += self.vel_y

		# rotation
		self.deg += self.rot_speed
		if self.deg >= 360:
			self.deg -= 360
		elif self.deg < 0:
			self.deg += 360

		if -self.size//2 < self.y < height+self.size//2:
			return False
		else:
			return True
	
	def draw(self, screen):
		# Rotate the rectangle
		rotated_surf = pygame.transform.rotate(self.surf, self.deg)

		# Get the new rect after rotation to center it
		rotated_rect = rotated_surf.get_rect(center=(self.x, self.y))

		# Blit the rotated rectangle to the screen
		screen.blit(rotated_surf, rotated_rect.topleft)
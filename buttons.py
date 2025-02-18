import pygame


pygame.font.init()

FONT = pygame.font.SysFont('Arial', 50)

#button class
class Button():
	def __init__(self, x, y, size, text):
		self.text = FONT.render(text,1,'white')
		self.horizontal_size = self.text.get_height()
		self.vertical_size = self.text.get_width()
		self.rect = pygame.Rect(x,y, self.vertical_size, self.horizontal_size)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		# if pygame.mouse.get_pressed()[0] == 0:
		# 	self.clicked = False

		#draw button on screen
		surface.blit(self.text, (self.rect.x, self.rect.y))
		pygame.draw.rect(surface, 'yellow', self.rect, 2)

		return action
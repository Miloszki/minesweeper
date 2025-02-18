import pygame


pygame.font.init()

FONT = pygame.font.SysFont('Arial', 50)

#button class
class Button():
	def __init__(self, x, y, text):
		self.text = FONT.render(text,1,'white')
		self.vertical_size = self.text.get_height()
		self.horizontal_size = self.text.get_width()
		self.rect = pygame.Rect(x - self.horizontal_size/2, y, self.horizontal_size, self.vertical_size)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True


		#draw button on screen
		surface.blit(self.text, (self.rect.x, self.rect.y))
		# pygame.draw.rect(surface, 'yellow', self.rect, 2) #debugging

		return action
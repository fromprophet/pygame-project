import pygame

class Character(object):
    def __init__(self, fontname, color):
        super().__init__()
        self.fontname = fontname
        self.color = color
        self.font = self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.text = self.font.render(self.fontname, True, self.color)
        self.rect = self.text.get_rect()
import pygame

class Question(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()

class Board(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert()
import pygame

class Question(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (200, 200)) 
        
class Answer(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (200, 200)) 
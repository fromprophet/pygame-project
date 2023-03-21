import pygame

class Item(object):
    # 空白0 水滴1 闪电2
    def __init__(self, index):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/item" + str(index) + ".png").convert_alpha(), (80, 80))
        self.index = index
        
class Player(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (80, 80))
        
class Board(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert()
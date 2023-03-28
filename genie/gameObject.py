import pygame

class Chessboard(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()

class SpriteItem(object):
    def __init__(self, screen, index):
        super().__init__()
        self.screen = screen
        self.index = index # 图片编号 0黄 1棕 2蓝 3红 4绿
        self.property = 1 # 显示图片模式。1正面 2背面
        self.listindex = [] # 用数组保存该图片显示在第几行第几个
        self.image1 = pygame.transform.scale(pygame.image.load("images/sprite" + str(index) + ".png").convert_alpha(), (80, 80)) # 正面图片
        self.image2 = pygame.transform.scale(pygame.image.load("images/questionmark.png").convert_alpha(), (80, 80)) # 背面图片
    
    def show(self):
        if self.property == 1:
            self.screen.blit(self.image1, ((self.listindex[1] * 80 + 90), (self.listindex[0] * 80 + 150)))
        elif self.property == 2:
            self.screen.blit(self.image2, ((self.listindex[1] * 80 + 90), (self.listindex[0] * 80 + 150)))
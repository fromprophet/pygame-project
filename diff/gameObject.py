import pygame

class Cube(object):
    def __init__(self, screen, index, level, colorlist = []):
        self.screen = screen
        self.index = index # 保存在第几行第几个
        self.colorlist = colorlist
        self.level = level
        self.sidewidth = 576 # 经计算，两边总宽高为576最好, 怎么除都是整数
        self.image = pygame.image.load("images/chessboard.png").convert_alpha()
        self.image1 = pygame.image.load("images/chessboard1.png").convert_alpha()
        
    def show(self):
        # 先画9个色块再画外边框
        # if len(self.colorlist) == 9:
        #     for i in range(len(self.colorlist)):
        #         pygame.draw.rect(self.screen, self.colorlist[i], ((i % 3) * 100, (i // 3) * 100, 100, 100), width = 100)
        #         self.screen.blit(pygame.transform.scale(self.image, (100, 100)), ((i % 3) * 100, (i // 3) * 100)) # 小块边框
        self.screen.blit(pygame.transform.scale(self.image, ((self.sidewidth / (self.level * 4)), (self.sidewidth / (self.level * 4)))), ( ((self.sidewidth / (self.level * 4)) * self.index[1]) + 50, ((self.sidewidth / (self.level * 4)) * self.index[0]) + 112)) # 大块边框
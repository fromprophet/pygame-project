import pygame

class Cube(object):
    # 小魔方
    def __init__(self, screen, index, level, colorlist = []):
        self.screen = screen
        self.index = index # 保存在第几行第几个
        self.colorlist = colorlist
        self.level = level
        self.sidewidth = 576 # 经计算，大图片两边总宽高为576最好, 怎么除都是整数
        self.image = pygame.image.load("images/chessboard.png").convert_alpha()
        self.image1 = pygame.image.load("images/chessboard1.png").convert_alpha()
        self.blockwidth = (self.sidewidth / (self.level * 4)) # 单个魔方块的宽高
        self.singlewidth = (self.blockwidth / 3) # 单个小色块的宽高
        
    def show(self, extendwidth):
        # 先画9个色块再画外边框
        if len(self.colorlist) == 9:
            for i in range(len(self.colorlist)):
                pygame.draw.rect(self.screen, self.colorlist[i], ((self.blockwidth * self.index[1]) + 50 + extendwidth + (i % 3) * self.singlewidth, (self.blockwidth * self.index[0]) + 112 + (i // 3) * self.singlewidth, self.singlewidth, self.singlewidth), width = 100) # 色块
                self.screen.blit(pygame.transform.scale(self.image1, (self.singlewidth, self.singlewidth)), ((self.blockwidth * self.index[1]) + 50 + extendwidth + (i % 3) * self.singlewidth, (self.blockwidth * self.index[0]) + 112 + (i // 3) * self.singlewidth)) # 小块边框
        self.screen.blit(pygame.transform.scale(self.image, (self.blockwidth , self.blockwidth)), ((self.blockwidth * self.index[1]) + 50 + extendwidth, (self.blockwidth * self.index[0]) + 112)) # 大块边框
        
class Board(object):
    # 外部边框
    def __init__(self, screen, index, level, property):
        self.screen = screen
        self.index = index
        self.level = level
        self.property = property # right:绿框 wrong:红框
        self.image1 = pygame.image.load("images/wrongcube.png").convert_alpha()
        self.image2 = pygame.image.load("images/rightcube.png").convert_alpha()
        self.sidewidth = 576 # 经计算，大图片两边总宽高为576最好, 怎么除都是整数
        self.blockwidth = (self.sidewidth / (self.level * 4)) # 单个魔方块的宽高
        
    def show(self, extendwidth):
        if self.property == "wrong":
            self.screen.blit(pygame.transform.scale(self.image1, (self.blockwidth , self.blockwidth)), ((self.blockwidth * self.index[1]) + 50 + extendwidth, (self.blockwidth * self.index[0]) + 112)) # 大块边框
        elif self.property == "right":
            self.screen.blit(pygame.transform.scale(self.image2, (self.blockwidth , self.blockwidth)), ((self.blockwidth * self.index[1]) + 50 + extendwidth, (self.blockwidth * self.index[0]) + 112))
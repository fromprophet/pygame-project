import pygame

class Chessboard(object):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()

class NumberFont(object):
    def __init__(self, num, property, index, chessboard_index):
        super().__init__()
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.numfont = self.font.render(str(num), True, (0, 0, 0))
        self.property = property # prime素数 composite合数
        self.index = index # 在棋盘的第几个位置
        self.chessboard_index = chessboard_index
        self.rect = self.numfont.get_rect()
        self.rect.width = 100
        self.rect.height = 100
        self.__getpos__()

    def __getpos__(self):
        x = self.index % self.chessboard_index
        y = self.index // self.chessboard_index
        self.rect.centerx = (x * 100) + (900 - 100 * self.chessboard_index) / 2 + 75
        self.rect.centery = (y * 100) + (700 - 100 * self.chessboard_index) / 2 + 75
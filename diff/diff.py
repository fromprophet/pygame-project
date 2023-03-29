import pygame
import sys
import random
import math
from gameObject import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Diff(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1600, 800))
        self.clock = pygame.time.Clock()
        self.colorlist = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF", "#FFFF00", "#FFA500"] # 魔方的6个颜色：红绿蓝白黄橙
        self.level = 6 # 设置游戏难度 每个难度下，魔方墙总个数为(self.level * 4) ** 2个
        self.sidewidth = 576 # 经计算，两边总宽高为576最好, 怎么除都是整数
        self.cubelist = [] # 存放所有的Cube对象
        self.__setcube__()
        
    def __setcube__(self):
        # 出题
        for i in range(self.level * 4):
            for j in range(self.level * 4):
                templist = []
                for index in range(9):
                    randindex = random.randint(0, 5)
                    templist.append(self.colorlist[randindex])
                cube = Cube(self.screen, [i, j], self.level, templist)
                self.cubelist.append(cube)
        
    def startGame(self):
        while True:
            self.clock.tick(60)
            self.__eventhanlder__()
            self.__update__()
            pygame.display.flip()
            
    def __eventhanlder__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def __update__(self):
        self.screen.fill("#808080")
        # 显示魔方墙
        for i in range(len(self.cubelist)):
            self.cubelist[i].show()
        
def diffGame():
    diff = Diff()
    diff.startGame()
    
if __name__ == "__main__":
    diffGame()
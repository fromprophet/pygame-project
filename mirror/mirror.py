import pygame
import sys
import time
import random
from gameObject import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Mirror(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.time = pygame.time.Clock()
        self.chessboard_index = 5 # 控制产生几*几的棋盘
        
        self.mirrorcount = random.randint(5, 10)
        self.randommirrorpos = random.sample([i for i in range(0, self.chessboard_index ** 2)], self.mirrorcount) # 随机位置
        self.__createbasicroles__()
        
        self.randbuttonindexX, self.randbuttonindexY = self.__setbuttonindex__()
        self.buttonlist = []
        self.buttonGroup = pygame.sprite.Group()
        self.__createbutton__()
        
        self.lightGroup = pygame.sprite.Group()
        self.__createlight__()
        
    def __createbasicroles__(self):
        # 棋盘和镜子生成
        self.chessboard = ChessBoard("images/chessboard.png").image
        self.reflectlist = []
        for i in range(self.mirrorcount):
            self.reflectlist.append(Reflect(random.randint(1, 2))) # 显示镜子
    
    def __setbuttonindex__(self):
        # 随机生成手电筒位置
        randbuttonindexX = random.randint(0, 3)
        randbuttonindexY = random.randint(0, self.chessboard_index - 1)
        while self.__judgebuttonindex__(randbuttonindexX, randbuttonindexY) == True:
            randbuttonindexX = random.randint(0, 3)
            randbuttonindexY = random.randint(0, self.chessboard_index - 1)
        return randbuttonindexX, randbuttonindexY
    
    def __judgebuttonindex__(self, x, y):
        # 手电筒随机后进行判断，如果没有经过任何镜面，就需要再次进行一次随机
        # x：上下左右 y:第几个 x = 0 or x = 1:找列  x = 2 or x = 3 找行
        flag = True
        for i in range(len(self.randommirrorpos)):
            if x == 0 or x == 1:
                if self.randommirrorpos[i] % self.chessboard_index == y:
                    flag = False
                    break
            elif x == 2 or x == 3:
                if self.randommirrorpos[i] // self.chessboard_index == y:
                    flag = False
                    break
        return flag
    def __createbutton__(self):
        # 创建按钮
        for i in range(0, 4):
            temp = []
            for j in range(0, self.chessboard_index):
                button = Button("button", i, True)
                if i == self.randbuttonindexX and j == self.randbuttonindexY:
                    button = Button("flash", i, True)
                if i >= 0 and i <= 1:
                    button.rect.x = (j % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2
                    button.rect.y = (i % 2) * (100 * (self.chessboard_index + 1)) + (800 - 100 * (self.chessboard_index + 2)) / 2
                elif i >= 2 and i <= 3:
                    button.rect.x = (i % 2) * (100 * (self.chessboard_index + 1)) + (900 - 100 * (self.chessboard_index + 2)) / 2
                    button.rect.y = (j % self.chessboard_index) * 100 + (800 - 100 * self.chessboard_index) / 2
                temp.append(button)
            self.buttonlist.append(temp)
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                self.buttonGroup.add(self.buttonlist[i][j])
                
    def __createlight__(self):
        # 创建光束及找到初始位置
        light = Light(self.randbuttonindexX, 10)
        # 接下来找到手电筒的下标
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if self.buttonlist[i][j].property == "flash":
                    rect = self.buttonlist[i][j].rect
                    break
        if light.index == 0:
            light.rect.centerx = rect.centerx
            light.rect.centery = rect.centery + 50
        elif light.index == 1:
            light.rect.centerx = rect.centerx
            light.rect.centery = rect.centery - 50
        elif light.index == 2:
            light.rect.centerx = rect.centerx + 50
            light.rect.centery = rect.centery
        elif light.index == 3:
            light.rect.centerx = rect.centerx - 50
            light.rect.centery = rect.centery
            
        self.lightGroup.add(light)
                  
    def startGame(self):
        while True:
            self.time.tick(60)
            self.__eventhandler__()
            self.__update__()
            pygame.display.flip()
            
    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        for i in range(0, self.chessboard_index ** 2):
            self.screen.blit(self.chessboard, ((i % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (i // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2)) # 显示棋盘
            
        for i in range(len(self.randommirrorpos)):
            self.screen.blit(self.reflectlist[i].image, ((self.randommirrorpos[i] % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (self.randommirrorpos[i] // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2)) # 显示镜子     
        
        for group in [self.buttonGroup, self.lightGroup]:
            group.update()
            group.draw(self.screen)
        
        
def main():
    mirror = Mirror()
    mirror.startGame()
    
if __name__ == "__main__":
    main()
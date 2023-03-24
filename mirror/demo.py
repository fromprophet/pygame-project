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
        self.randommirrorpos = random.sample([i for i in range(0, self.chessboard_index ** 2)], self.mirrorcount) # 随机镜子位置 得到下标列表
        self.__createbasicroles__()
        
        self.randbuttonindexX, self.randbuttonindexY = self.__setbuttonindex__()
        self.buttonlist = []
        self.buttonGroup = pygame.sprite.Group() # 按钮精灵组
        self.flashGroup = pygame.sprite.Group() # 手电筒精灵组 二者分离开以便做按钮和光束的碰撞
        self.__createbutton__()
        
        self.lightGroup = pygame.sprite.Group()
        self.__createlight__()
        
    def __createbasicroles__(self):
        # 棋盘和镜子生成
        self.chessboard = ChessBoard("images/chessboard.png").image
        self.reflectlist = []
        for i in range(self.mirrorcount):
            reflect = Reflect(random.randint(1, 2), self.randommirrorpos[i])
            reflect.rect.topleft = [(self.randommirrorpos[i] % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (self.randommirrorpos[i] // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2]
            self.reflectlist.append(reflect) # 显示镜子
    
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
                
                button.indexposition = [i, j]
                temp.append(button)
            self.buttonlist.append(temp)
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if self.buttonlist[i][j].property == "button":
                    self.buttonGroup.add(self.buttonlist[i][j])
                elif self.buttonlist[i][j].property == "flash":
                    self.flashGroup.add(self.buttonlist[i][j])
                
    def __createlight__(self):
        # 创建光束及找到初始位置
        self.light = Light(self.randbuttonindexX, 10)
        # 接下来找到手电筒的下标
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if self.buttonlist[i][j].property == "flash":
                    rect = self.buttonlist[i][j].rect
                    break
        if self.light.index == 0:
            self.light.rect.centerx = rect.centerx
            self.light.rect.centery = rect.centery + 50
        elif self.light.index == 1:
            self.light.rect.centerx = rect.centerx
            self.light.rect.centery = rect.centery - 50
        elif self.light.index == 2:
            self.light.rect.centerx = rect.centerx + 50
            self.light.rect.centery = rect.centery
        elif self.light.index == 3:
            self.light.rect.centerx = rect.centerx - 50
            self.light.rect.centery = rect.centery
            
        self.lightGroup.add(self.light)
        self.lightpointlist = [] # 存储光线（多条直线）坐标
        self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery]) # 画光线。给出初始坐标
                  
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
            self.screen.blit(self.reflectlist[i].image, self.reflectlist[i].rect)
        
        self.__update_light_index__()
        
        for group in [self.buttonGroup, self.flashGroup, self.lightGroup]:
            group.update()
            group.draw(self.screen)
            
    def __update_light_index__(self):
        # 进行光的反射
        # 根据光“精灵”位置更新坐标列表，以便画光线
        if len(self.lightpointlist) == 1:
            self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery])
        elif len(self.lightpointlist) > 1:
            self.lightpointlist.pop(-1)
            self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery])
        # 首先找到光在哪个格子里
        self.lightpos = ((self.light.rect.centery - ((800 - 100 * self.chessboard_index) / 2)) // 100) * self.chessboard_index + ((self.light.rect.centerx - ((900 - 100 * self.chessboard_index) / 2)) // 100)
        # 接下来把光和镜子中心点进行判断
        if self.lightpos in self.randommirrorpos:
            # （1）如果碰到了镜子，需要找到镜子的下标
            for i in range(len(self.reflectlist)):
                if self.lightpos == self.reflectlist[i].index:
                    temp = self.reflectlist[i]
                    break
            if self.light.rect.centerx == temp.rect.centerx and self.light.rect.centery == temp.rect.centery:
                # （2） 判断方向及属性，改变光的index
                if self.light.index == 0: # 从上向下射
                    if temp.property == 1:
                        self.light.index = 3
                    elif temp.property == 2:
                        self.light.index = 2
                elif self.light.index == 1: # 从下向上射
                    if temp.property == 1:
                        self.light.index = 2
                    elif temp.property == 2:
                        self.light.index = 3
                elif self.light.index == 2: # 从左向右射
                    if temp.property == 1:
                        self.light.index = 1
                    elif temp.property == 2:
                        self.light.index = 0
                elif self.light.index == 3: # 从右向左射
                    if temp.property == 1:
                        self.light.index = 0
                    elif temp.property == 2:
                        self.light.index = 1
                self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery]) # 遇到转折处打点
                
        self.__lightcollide__()
        # （3）根据光的index改方向
        self.light.directionX, self.light.directionY = self.light.setdirection()
            
        pygame.draw.lines(self.screen, 'black', False, self.lightpointlist, width = 1) # 用drawlines画光线
        
    def __lightcollide__(self):
        # 光线和按钮碰撞检测
        collision = pygame.sprite.groupcollide(self.lightGroup, self.buttonGroup, True, False) # 后两个bool值分别表示这两个精灵组如发生碰撞是否删除
        for button_sprite in collision.values():
            print(button_sprite[0].indexposition)

def main():
    mirror = Mirror()
    mirror.startGame()
    
if __name__ == "__main__":
    main()
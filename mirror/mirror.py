import pygame
import sys
import time
import random
from gameObject import *
from gamePart import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Mirror(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.time = pygame.time.Clock()
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.chessboard_index = 5 # 控制产生几*几的棋盘
        self.mode = "memory" # 控制单题游戏阶段。memory记忆阶段 select选择做题阶段 showresult展示结果阶段
        
        self.mirrorcount = random.randint(5, 10) # 随机镜子个数
        self.randommirrorpos = random.sample([i for i in range(0, self.chessboard_index ** 2)], self.mirrorcount) # 随机镜子位置 得到下标列表
        self.memory = Memory(self.screen, self.chessboard_index, self.mirrorcount, self.randommirrorpos)
        self.select = Select(self.screen, self.chessboard_index, self.randommirrorpos)
        self.showresult = Showresult(self.screen, self.chessboard_index, self.randommirrorpos, self.memory.reflectlist, self.select.buttonlist, [], self.select.buttonGroup, self.select.flashGroup)
        self.playeranswer = [] # 如用户点击了按钮，保存结果[方向，个数]
        
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
            
            if self.mode == "memory":
                self.memory.eventhandler(event)
            elif self.mode == "select":
                self.select.eventhandler(event)
                self.playeranswer = self.select.playeranswer
        if self.memory.mode == "select":
            self.mode = "select"
        if self.select.mode == "showresult":
            self.mode = "showresult"
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        
        if self.mode == "memory":
            self.memory.updateroles()
        elif self.mode == "select":
            self.select.updateroles()
        elif self.mode == "showresult":
            self.showresult.updateroles()
        
def main():
    mirror = Mirror()
    mirror.startGame()
    
if __name__ == "__main__":
    main()
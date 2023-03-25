import pygame
import sys
import time
import random
import math
from gameObject import *
from gamePart import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
bgm = pygame.mixer.music.load("sounds/bgm.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(999)

class Ready(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 72)
        self.gametime = 3
        self.colorlist = [['#0000FF', '#FFFF00'], ['#00FF00', '#0000FF'], ['#FF0000', '#00FF00'], ['#000000', '#808080']]
        self.second_sound = pygame.mixer.Sound("sounds/second.mp3")
        self.second_sound.set_volume(0.3)
        self.starttime = time.time()
        self.endtime = time.time()

    def startGame(self):
        self.second_sound.play()
        while True:
            self.__enentHandler__()
            self.__update__()
            pygame.display.flip()

    def __enentHandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __timeget__(self):
        # 通过time.time()读秒
        self.endtime = time.time()
        if self.gametime >= 1:
            if self.endtime - self.starttime >= 1.0:
                self.gametime -= 1
                self.starttime = time.time()
                self.second_sound.play()
        
        if self.gametime <= 0:
            self.second_sound.stop()
            mirror = Mirror()
            mirror.startGame()
            
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        text = self.font.render(str(self.gametime), True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (400, 350)
        self.__timeget__()
        pygame.draw.circle(self.screen, self.colorlist[3 - self.gametime][0], (400, 350), 200, width = 200)
        pygame.draw.arc(self.screen, self.colorlist[3 - self.gametime][1], (200, 150, 400, 400), math.radians(90), math.radians(1 - (self.endtime - self.starttime) * 360 + 90), width = 400) # rect参数： left, top, width, height
        self.screen.blit(text, textrect)

class Mirror(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.time = pygame.time.Clock()
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.chessboard_index = 5 # 控制产生几*几的棋盘
        self.mode = "memory" # 控制单题游戏阶段。memory记忆阶段 select选择做题阶段 showresult展示结果阶段
        
        self.__setquestion__()

        self.questionsum = 10 # 一共多少题
        self.questionnum = 1 # 已做到第几题
        self.correctnum = 0 # 已做对几道题

        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)

    def __setquestion__(self):
        # 出题
        self.mirrorcount = random.randint(5, 10) # 随机镜子个数
        self.randommirrorpos = random.sample([i for i in range(0, self.chessboard_index ** 2)], self.mirrorcount) # 随机镜子位置 得到下标列表
        self.memory = Memory(self.screen, self.chessboard_index, self.mirrorcount, self.randommirrorpos)
        self.select = Select(self.screen, self.chessboard_index, self.randommirrorpos)
        self.showresult = Showresult(self.screen, self.chessboard_index, self.randommirrorpos, self.memory.reflectlist, self.select.buttonlist, [], self.select.buttonGroup, self.select.flashGroup)
        
    def startGame(self):
        self.start_sound.play()
        while True:
            self.time.tick(60)
            self.__modeselect__()
            self.__eventhandler__()
            self.__update__()
            pygame.display.flip()
    
    def __modeselect__(self):
        # 单题中模式的切换。memory：记忆阶段 select：选择阶段 showresult：显示结果阶段
        if self.memory.mode == "select":
            self.mode = "select"
        if self.select.mode == "showresult":
            self.mode = "showresult"
        if self.showresult.mode == "memory" and self.showresult.changemodeflag == True:
            if self.showresult.playerflag == 1:
                self.correctnum += 1
            self.questionnum += 1
            self.showresult.playerflag = 0 # 把showresult类中playerflag属性调为0，否则会一直运行此段代码，一直在刷
            self.showresult.changemodeflag = False
            if self.questionnum <= self.questionsum:
                self.__setquestion__() # 出新题
                self.mode = "memory"
            else:
                result = Result(self.questionsum, self.correctnum)
                result.startGame()
            
    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.mode == "memory":
                self.memory.eventhandler(event)
            elif self.mode == "select":
                self.select.eventhandler(event)
                self.showresult.playeranswer = self.select.playeranswer
        
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        
        if self.mode == "memory":
            self.memory.updateroles()
        elif self.mode == "select":
            self.select.updateroles()
        elif self.mode == "showresult":
            self.showresult.updateroles()

        # 显示题目数量和正确题数
        self.questionfont = self.font.render("题目数量：" + str(self.questionnum) + "/" + str(self.questionsum), True, 'black')
        self.correctnumfont = self.font.render("正确题数：" + str(self.correctnum), True, 'black')
        self.questionfont_rect = self.questionfont.get_rect()
        self.questionfont_rect.top = 0
        self.questionfont_rect.left = 0
        self.correctnumfont_rect = self.correctnumfont.get_rect()
        self.correctnumfont_rect.top = 0
        self.correctnumfont_rect.right = 900
        self.screen.blit(self.questionfont, self.questionfont_rect)
        self.screen.blit(self.correctnumfont, self.correctnumfont_rect)

class Result(object):
    # 显示结果
    def __init__(self, sum, correctnum):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.sum = sum
        self.correctnum = correctnum

    def startGame(self):
        while True:
            self.__eventhandler__()
            self.__update__()
            pygame.display.flip()

    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressedArr = pygame.mouse.get_pressed()
                for index in range(len(pressedArr)):
                    if index == 0 and pressedArr[index]:
                        pos = pygame.mouse.get_pos()
                        posX = pos[0]
                        posY = pos[1]
                        if posX > 500 and posX < 700 and posY > 450 and posY < 550:
                            ready = Ready()
                            ready.startGame()

    def __update__(self):
        self.screen.fill("#808080")
        text1 = self.font.render("任务完成", True, (0, 0, 0))
        text2 = self.font.render("你的正确题数：" + str(self.correctnum) + "   正确率：" + str(round(self.correctnum / self.sum * 100, 2)) + "%", True, (0, 0, 0))
        self.screen.blit(text1, (150, 150))
        self.screen.blit(text2, (150, 250))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))
        
def main():

    ready = Ready()
    ready.startGame()

if __name__ == "__main__":
    main()
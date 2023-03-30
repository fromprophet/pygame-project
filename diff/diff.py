import pygame
import sys
import random
import math
import time
from gameObject import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class DiffReady(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1600, 800))
        pygame.display.set_caption("魔方墙找茬")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 72)
        self.gametime = 3
        self.colorlist = [['#0000FF', '#FFFF00'], ['#00FF00', '#0000FF'], ['#FF0000', '#00FF00'], ['#000000', '#808080']]
        self.second_sound = pygame.mixer.Sound("sounds/second.mp3")
        self.second_sound.set_volume(0.4)
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
            diff = Diff()
            diff.startGame()

    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (1300, 0))
        text = self.font.render(str(self.gametime), True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (400, 350)
        self.__timeget__()
        pygame.draw.circle(self.screen, self.colorlist[3 - self.gametime][0], (400, 350), 200, width = 200)
        pygame.draw.arc(self.screen, self.colorlist[3 - self.gametime][1], (200, 150, 400, 400), math.radians(90), math.radians(1 - (self.endtime - self.starttime) * 360 + 90), width = 400) # rect参数： left, top, width, height
        self.screen.blit(text, textrect)

class Diff(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1600, 800))
        pygame.display.set_caption("魔方墙找茬")
        self.clock = pygame.time.Clock()
        self.colorlist = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF", "#FFFF00", "#FFA500"] # 魔方的6个颜色：红绿蓝白黄橙
        self.level = 1 # 设置游戏难度 每个难度下，魔方墙总个数为(self.level * 4) ** 2个
        self.sidewidth = 576 # 经计算，两边总宽高为576最好, 怎么除都是整数
        
        self.hoverindex = 0 # hover的图片（0未hover 1左 2右）
        self.hovercube = [] # hover的魔方下标
        self.iscomplete = 0 # 1已通关 2未通关
        self.__setcube__()
        
    def __setcube__(self):
        # 出题
        self.cubelist = [] # 存放所有的Cube对象
        self.temp_property = 0 # 0未作答 1作对 2做错
        self.clickmode = "" # 做完一题后如对了进入下一题，错了进入结算，通关了也进入结算
        for i in range(self.level * 4):
            for j in range(self.level * 4):
                templist = []
                for index in range(9):
                    randindex = random.randint(0, 5)
                    templist.append(self.colorlist[randindex])
                cube = Cube(self.screen, [i, j], self.level, templist)
                self.cubelist.append(cube)
        self.__setquestion__()
        
    def __setquestion__(self):
        # 设置茬
        self.randx = random.randint(0, self.level * 4 - 1)
        self.randy = random.randint(0, self.level * 4 - 1)
        self.randindex = self.randx * self.level * 4 + self.randy
        print(self.randindex, [self.randx, self.randy])
        # temp_colorlist = self.cubelist[self.randx * self.level * 4 + self.randy].colorlist
        temp_colorlist = []
        for i in range(len(self.cubelist[self.randindex].colorlist)):
            temp_colorlist.append(self.cubelist[self.randindex].colorlist[i]) # 个人疑问点：不能直接赋值，需要手动一个个往空列表里录。否则的话后面的改变会连带着原图一起改变
        temp_indexlist = random.sample([i for i in range(0, 9)], (self.level * 2)) # 动态难度设置。每个难度改动的色块分别为：1 3 5 7 9或 2 4 6 8
        # print(temp_colorlist, self.cubelist[self.randindex].colorlist)
        for i in range(len(temp_indexlist)):
            temp_colorlist[temp_indexlist[i]] = self.__randcolor__(temp_colorlist[temp_indexlist[i]])
        # print(self.cubelist[self.randindex].colorlist)
        # print(temp_colorlist, [self.randx, self.randy])
        self.tempcube = Cube(self.screen, [self.randx, self.randy], self.level, temp_colorlist)
            
    def __randcolor__(self, color):
        color = color
        res = random.choice(self.colorlist)
        if res != color:
            return res
        elif res == color:
            return self.__randcolor__(color)
        
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
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                posx = pos[0]
                posy = pos[1]
                self.hoverindex = self.__gethoverindex__(posx, posy)
                if self.hoverindex != 0:
                    self.hovercube = self.__gethovercube__(posx, posy)
                elif self.hoverindex == 0:
                    self.hovercube = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                keyarr = pygame.mouse.get_pressed()
                for index in range(len(keyarr)):
                    if keyarr[index] and index == 0:
                        keypos = pygame.mouse.get_pos()
                        if keypos[0] > 550 and keypos[0] < 710 and keypos[1] > 700 and keypos[1] < 780:
                            if self.clickmode == "nextlevel":
                                self.level += 1
                                self.__setcube__() # 重新出题
                            elif self.clickmode == "result":
                                result = Result(self.level, self.iscomplete)
                                result.startGame()
                        else:
                            keyindex = self.__gethoverindex__(keypos[0], keypos[1])
                            if keyindex != 0 and self.temp_property == 0:
                                self.keycube = self.__gethovercube__(keypos[0], keypos[1])
                            elif keyindex == 0:
                                self.keycube = []
                            if keyindex != 0 and len(self.keycube) != 0:
                                    if self.keycube == [self.randx, self.randy]:
                                        self.temp_property = 1
                                    else:
                                        self.temp_property = 2
                                    
    def __gethoverindex__(self, x, y):
        # 找到鼠标在哪个图像上
        if x > 50 and x < 626 and y > 112 and y < 688:
            return 1
        elif x > 674 and x < 1250 and y > 112 and y < 688:
            return 2
        else:
            return 0
        
    def __gethovercube__(self, x, y):
        # 找到鼠标在哪个小魔方上
        cubewidth = self.sidewidth / (self.level * 4) # 单个魔方宽高
        if self.hoverindex == 1:
            indexx = int((x - 50) // cubewidth)
        elif self.hoverindex == 2:
            indexx = int((x - 674) // cubewidth)
        indexy = int((y - 112) // cubewidth)
        return [indexy, indexx] # 表示鼠标在第几行第几个魔方上
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (1300, 0))
        # 显示魔方墙
        for i in range(len(self.cubelist)):
            self.cubelist[i].show(0)
        # 显示右侧魔方墙 画“茬”
        for i in range(0, len(self.cubelist)):
            if i == self.randindex:
                self.tempcube.show(624)
                # print(i)
            else:
                self.cubelist[i].show(624)
        # 显示hover框
        if self.hoverindex != 0 and len(self.hovercube) != 0:
            board = Board(self.screen, self.hovercube, self.level, "wrong")
            board.show(0)
            board.show(624)
        # 显示绿框或红框、对勾或叉号、以及“下一题”或“进入结算”按钮
        if self.temp_property != 0:
            if self.temp_property == 1:
                rightboard = Board(self.screen, self.keycube, self.level, "right")
                rightboard.show(0)
                rightboard.show(624)
                
                self.screen.blit(pygame.transform.scale(pygame.image.load("images/right.png").convert_alpha(), (150, 110)), (600, 500))
                
                if self.level < 4:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("images/nextlevel.png").convert_alpha(), (160, 80)), (550, 700))
                    self.clickmode = "nextlevel"
                else:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("images/result.png").convert_alpha(), (160, 80)), (550, 700))
                    self.clickmode = "result"
                    self.iscomplete = 1
            elif self.temp_property == 2:
                wrongboard = Board(self.screen, self.keycube, self.level, "wrong")
                wrongboard.show(0)
                wrongboard.show(624)
                
                self.screen.blit(pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110)), (600, 500))
                
                self.screen.blit(pygame.transform.scale(pygame.image.load("images/result.png").convert_alpha(), (160, 80)), (550, 700))
                self.clickmode = "result"
                self.iscomplete = 2

class Result(object):
    # 显示结果
    def __init__(self, level, iscomplete):
        super().__init__()
        self.screen = pygame.display.set_mode((1600, 800))
        pygame.display.set_caption("魔方墙找茬")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.sum = sum
        self.level = level
        self.iscomplete = iscomplete # 是否通关
        self.__setfonts__()
        
    def __setfonts__(self):
        if self.iscomplete == 1:
            self.text1 = self.font.render("恭喜通关！", True, (0, 0, 0))
            self.text2 = self.font.render("已完成所有难度", True, (0, 0, 0))
        elif self.iscomplete == 2:
            self.text1 = self.font.render("任务结束", True, (0, 0, 0))
            self.text2 = self.font.render("已达到难度" + str(self.level), True, (0, 0, 0))
        
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
                            ready = DiffReady()
                            ready.startGame()

    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(self.text1, (150, 150))
        self.screen.blit(self.text2, (150, 250))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))                
        
def diffGame():
    # diff = Diff()
    # diff.startGame()
    ready = DiffReady()
    ready.startGame()
    
if __name__ == "__main__":
    diffGame()
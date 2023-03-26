import pygame
import sys
import time
import random
import math
from gameobject import *

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.mixer.music.load("sounds/bgm.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(999)

class Ready(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("闪电躲避")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 72)
        self.description = Board("images/description.png").image
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
            dodge = Dodge()
            dodge.startGame()

    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(self.description, (900, 0))
        text = self.font.render(str(self.gametime), True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (400, 350)
        self.__timeget__()
        pygame.draw.circle(self.screen, self.colorlist[3 - self.gametime][0], (400, 350), 200, width = 200)
        pygame.draw.arc(self.screen, self.colorlist[3 - self.gametime][1], (200, 150, 400, 400), math.radians(90), math.radians(1 - (self.endtime - self.starttime) * 360 + 90), width = 400) # rect参数： left, top, width, height
        self.screen.blit(text, textrect)

class Dodge(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(((1200, 800)))
        pygame.display.set_caption("闪电躲避")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.__createroles__()
        self.playerpos = 0 # 角色初始位置 0左1右
        self.itempos = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]] # 保存所有可能的物品摆放位置。0 空地 1 水滴 2 闪电
        self.questionlist = [] # 保存所有物品的位置（二维列表）
        for i in range(0, 8):
            self.questionlist.append(self.__getrandomitems__()) # 初始化物品位置，填满所有格子
        self.correctnum = 0
        self.questionsum = 0 # 一共做了多少题
        self.questionnum = 0 # 一共做对了多少题
        self.wrongproperty = 0 # 如答错持续显示错号0.5秒钟，并在此期间无法作答
        self.start_wrongtime = 0
        self.end_wrongtime = 0
        self.sum_gametime = 20.0
        self.start_gametime = time.time()
        self.end_gametime = time.time()
        self.__createfonts__()
        
    def __createroles__(self):
        self.player = Player("images/umbrella.png").image
        self.itemlist = [Item(0), Item(1), Item(2)] # 0 空地 1 水滴 2 闪电

        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.waterdrop_sound = pygame.mixer.Sound("sounds/waterdrop.mp3")
        self.waterdrop_sound.set_volume(1.5)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)
        
    def __createfonts__(self):
        self.text1 = self.font.render("游戏时间：", True, "black")
        self.text2 = self.font.render("分数：", True, 'black')
        
    def __getrandomitems__(self):
        # 给一行赋随机的物品摆放
        index = random.randint(0, len(self.itempos) - 1)
        return self.itempos[index]
        
    def startGame(self):
        self.start_sound.play()
        while True:
            self.clock.tick(60)
            self.__eventhandler__()
            self.__updateroles__()
            pygame.display.flip()
            
    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.wrongproperty == 0:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if event.key == pygame.K_LEFT:
                            self.playerpos = 0
                        elif event.key == pygame.K_RIGHT:
                            self.playerpos = 1       
                        
                        self.questionsum += 1

                        self.start_sound.stop()
                        self.correct_sound.stop()
                        self.wrong_sound.stop()

                        if self.questionlist[0][self.playerpos] == 0:
                            self.correctnum += 1
                            self.questionnum += 1
                            self.correct_sound.play()
                        elif self.questionlist[0][self.playerpos] == 1:
                            self.correctnum += 5
                            self.questionnum += 1
                            self.waterdrop_sound.play()
                        elif self.questionlist[0][self.playerpos] == 2:
                            self.correctnum -= 10 # 答案判断 空地加1分；水滴加5分；闪电减10分
                            self.wrongproperty = 1
                            self.wrong_sound.play()
                            self.start_wrongtime = time.time()
                        if self.wrongproperty == 0:
                            self.questionlist.pop(0)
                            self.questionlist.append(self.__getrandomitems__())
                            
    def __updateroles__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        self.__drawblocks__()
        self.screen.blit(self.player, (self.playerpos * 80 + 350, 690))
        self.__drawitems__()
        # 如答错持续显示错号0.5秒钟，并在此期间无法作答
        if self.wrongproperty == 1:
            self.__drawwrong__()
            
        self.__drawboard__()
        self.end_gametime = time.time()
        if self.end_gametime - self.start_gametime >= self.sum_gametime:
            result = Result(self.questionsum, self.questionnum, self.correctnum)
            result.startGame()
        
    def __drawblocks__(self):
        # 一共画9*2共18个格子
        for i in range(18):
            pygame.draw.rect(self.screen, 'black', ((i % 2) * 80 + 350, (i // 2) * 80 + 50, 80, 80), width = 1)
            
    def __drawitems__(self):
        # 画所有的物品
        for i in range(len(self.questionlist)):
            for j in range(len(self.questionlist[i])):
                self.screen.blit(self.itemlist[self.questionlist[i][j]].image, ((j % 2) * 80 + 350, 560 - i * 80 + 50))
                
    def __drawwrong__(self):
        # 画错号，同时卡住游戏0.5秒
        self.end_wrongtime = time.time()
        if self.end_wrongtime - self.start_wrongtime <= 0.5:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110)), (410, 560))
        else:
            self.wrongproperty = 0
            self.questionlist.pop(0)
            self.questionlist.append(self.__getrandomitems__())
            
    def __drawboard__(self):
        # 局内计分板
        self.text_gametime = self.font.render(str(round(self.sum_gametime - (self.end_gametime - self.start_gametime), 2)), True, 'black')
        self.text_correctnum = self.font.render(str(self.correctnum * 10), True, 'black')
        textrect1 = self.text1.get_rect()
        textrect2 = self.text2.get_rect()
        textrect3 = self.text_gametime.get_rect()
        textrect4 = self.text_correctnum.get_rect()
        textrect1.top = textrect2.top = textrect3.top = textrect4.top = 0
        textrect1.left = 0
        textrect2.left = 700
        textrect3.left = 150
        textrect4.left = 800
        self.screen.blit(self.text1, textrect1)
        self.screen.blit(self.text2, textrect2)
        self.screen.blit(self.text_gametime, textrect3)
        self.screen.blit(self.text_correctnum, textrect4)

class Result(object):
    # 显示结果
    def __init__(self, sum, correctnum, score):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("闪电躲避")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.sum = sum
        self.correctnum = correctnum
        self.score = score

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
        text3 = self.font.render("你的得分："+ str(self.score * 10), True, (0, 0, 0))
        self.screen.blit(text1, (150, 150))
        self.screen.blit(text2, (150, 250))
        self.screen.blit(text3, (150, 350))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))

def main():
    ready = Ready()
    ready.startGame()

if __name__ == "__main__":
    main()
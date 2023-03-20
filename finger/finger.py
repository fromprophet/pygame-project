import pygame
import sys
import random
import time
import math
from gameObject import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/bgm.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(999)

class Ready(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
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
            finger = Finger()
            finger.startGame()

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


class Finger(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        self.__createroles__()
        self.questionsum = 10 # 一共多少题
        self.questionnum = 1 # 已做到第几题
        self.tempanswer = 0 # 保存每次答题时的答案
        self.tempproperty = 0 # 保存每次作答的对错。1对2错
        self.correctnum = 0
        self.rand = 999
        self.rand = self.__randindex__()
        self.start_property_time = 0 # 控制显示对勾和叉号的时间
        self.end_property_time = 0
        self.start_answer_time = time.time() # 以下4个参数控制单题作答时间、所有正确题目作答时间、以及平均作答时间
        self.end_answer_time = 0
        self.answer_time_list = []
        self.arr_answer_time = 0
        
    def __createroles__(self):
        self.questionlist = [Question("images/finger" + str(i) + ".png").image for i in range(0, 6)]
        self.answerlist = [Answer("images/answer" + str(i) + ".png").image for i in range(0, 3)]
        self.answerlist_green = [3, 1, 2] # 1石头2剪子3布 保存答案
        self.answerlist_red = [2, 3, 1]
        self.right_png = pygame.transform.scale(pygame.image.load("images/right.png").convert_alpha(), (150, 110))
        self.wrong_png = pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110))
        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)

    def __randindex__(self):
        temp = random.randint(0, len(self.questionlist) - 1)
        while temp == self.rand:
            temp = random.randint(0, len(self.questionlist) - 1)
        return temp
        
    def startGame(self):
        self.start_sound.play()
        while True:
            self.clock.tick(60)
            self.__eventHandler__()
            self.__updateRoles__()
            pygame.display.flip()
        
    def __eventHandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tempanswer == 0 and self.tempproperty == 0: # 此为防一直点鼠标卡死
                    indexarr = pygame.mouse.get_pressed()
                    for index in range(len(indexarr)):
                        if indexarr[index] and index == 0:
                            flag = 0
                            pos = pygame.mouse.get_pos()
                            posx = pos[0]
                            posy = pos[1]
                            if posx > 150 and posx < 350 and posy > 400 and posy < 600:
                                self.tempanswer = 1
                            elif posx > 370 and posx < 570 and posy > 400 and posy < 600:
                                self.tempanswer = 2
                            elif posx > 590 and posx < 790 and posy > 400 and posy < 600:
                                self.tempanswer = 3
                            if self.tempanswer != 0:
                                if self.start_sound.play():
                                    self.start_sound.stop()
                                self.start_property_time = time.time()
                                flag = self.__judgecorrection__(self.rand, self.tempanswer)
                            if flag == 1:
                                self.tempproperty = 1
                                self.correctnum += 1
                                self.correct_sound.play()
                                self.end_answer_time = time.time()
                                self.answer_time_list.append(self.end_answer_time - self.start_answer_time)
                            elif flag == 2:
                                self.tempproperty = 2
                                self.wrong_sound.play()
                        
    def __judgecorrection__(self, rand, tempanswer):
        # 判断做题是否正确 1对2错
        if rand >= 0 and rand <= 2:
            if tempanswer == self.answerlist_green[rand]:
                return 1
            else:
                return 2
        elif rand >= 3 and rand <= 5:
            if tempanswer == self.answerlist_red[rand - 3]:
                return 1
            else:
                return 2
                
    def __updateRoles__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        self.screen.blit(self.questionlist[self.rand], (325, 70))
        for i in range(len(self.answerlist)):
            self.screen.blit(self.answerlist[i], (150 + i * 220, 400)) # (150, 400) (370, 400) (590, 400) 宽高均为200 显示所有的答案图片

        if self.tempanswer != 0 and self.tempproperty != 0: # 显示对号或错号
            self.end_property_time = time.time()
            if self.end_property_time - self.start_property_time <= 1:
                self.__showproperty__(self.tempproperty)
            else:
                self.tempanswer = 0
                self.tempproperty = 0
                self.questionnum += 1
                if self.questionnum <= self.questionsum:
                    self.rand = self.__randindex__()
                    self.start_answer_time = time.time()
                else:
                    self.arr_answer_time = sum(self.answer_time_list) / len(self.answer_time_list)
                    result = Result(self.questionsum, self.correctnum, self.arr_answer_time)
                    result.startGame()

        self.__showboard__(self.questionsum, self.questionnum, self.correctnum)
    
    def __showproperty__(self, tempproperty):
        if tempproperty == 1:
            self.screen.blit(self.right_png, (475, 250))
        elif tempproperty == 2:
            self.screen.blit(self.wrong_png, (475, 250))

    def __showboard__(self, questionsum, questionnum, correctnum):
        self.screen.blit(pygame.image.load("images/correctnum.png").convert_alpha(), (0, 0))
        self.screen.blit(pygame.image.load("images/correctnum.png").convert_alpha(), (740, 0))
        self.screen.blit(pygame.image.load("images/number.png").convert_alpha(), (170, 0))
        ques_shiwei = str(int(self.questionnum // 10))
        ques_gewei = str(self.questionnum % 10)
        sum_shiwei = str(int(self.questionsum // 10))
        sum_gewei = str(self.questionsum % 10)
        corr_shiwei = str(int(self.correctnum // 10))
        corr_gewei = str(self.correctnum % 10)
        self.screen.blit(pygame.image.load("images/number_"+ ques_shiwei + ".png").convert_alpha(), (110, 0))
        self.screen.blit(pygame.image.load("images/number_"+ ques_gewei + ".png").convert_alpha(), (140, 0))
        self.screen.blit(pygame.image.load("images/number_"+ sum_shiwei + ".png").convert_alpha(), (200, 0))
        self.screen.blit(pygame.image.load("images/number_"+ sum_gewei + ".png").convert_alpha(), (230, 0))
        self.screen.blit(pygame.image.load("images/number_"+ corr_shiwei + ".png").convert_alpha(), (840, 0))
        self.screen.blit(pygame.image.load("images/number_"+ corr_gewei + ".png").convert_alpha(), (870, 0))

class Result(object):
    # 显示结果
    def __init__(self, sum, correctnum, arrange):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.sum = sum
        self.correctnum = correctnum
        self.arrange = arrange
        self.score = self.__countScore__(self.sum, self.correctnum, self.arrange)

    def __countScore__(self, sum, correctnum, arrange):
        wrong = sum - correctnum
        index = arrange ** -2
        res = sum * 1000 + int(correctnum * 500 * index) - wrong * 1000
        return res

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
        text2 = self.font.render("你的正确题数：" + str(self.correctnum) + "   平均作答时间：" + str(round(self.arrange, 3)) + "秒", True, (0, 0, 0))
        text3 = self.font.render("你的得分："+ str(self.score), True, (0, 0, 0))
        self.screen.blit(text1, (150, 150))
        self.screen.blit(text2, (150, 250))
        self.screen.blit(text3, (150, 350))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))


def main():
    # finger = Finger()
    # finger.startGame()
    ready = Ready()
    ready.startGame()
    
if __name__ == "__main__":
    main()
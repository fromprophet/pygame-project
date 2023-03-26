import pygame
import sys
import random
import time
import math
from gameObject import *

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
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("方向判断")
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
            arrow = Arrow()
            arrow.startGame()

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

class Arrow():
    # 游戏界面
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("方向判断")
        self.clock = pygame.time.Clock()
        self.question_sum = 10 # 题目总数
        self.question_num = 1 # 已做到第几题
        self.correct_num = 0
        self.temp_property = 0 # 1：这道题做对了 2：这道题做错了 0：做题阶段
        self.start_property_time = 0 # 控制显示对号叉号的显示时间
        self.end_property_time = 0
        self.__create_roles__()
        self.rand = 0 
        self.rand = self.__randnum__() # 随机第几题
        self.start_answer_time = time.time() # 保存一次做对题时所用的时间
        self.end_answer_time = 0
        self.answer_time_list = [] # 保存所有做题时间
        self.arrange_answer_time = 0 # 保存平均做题时间

    def __randnum__(self):
        temp = random.randint(0, len(self.question_list) - 1)
        while temp == self.rand:
            temp = random.randint(0, len(self.question_list) - 1) # 防止出现连续两次随机到同样的数
        else:
            return temp

    def __create_roles__(self):
        self.question_list = [Question("images/arrow" + str(i) + ".png").image for i in range(0, 8)]
        self.answer_green_list = [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]
        self.answer_red_list = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
        self.description = Board("images/description.png").image

        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)

    def startGame(self):
        """start game"""
        self.start_sound.play()
        while True:
            self.clock.tick(60)
            self.__eventhandler__()
            self.__update_roles__()
            pygame.display.flip()

    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.temp_property == 0: # 防一直按键盘卡死
                    if self.start_sound.play():
                        self.start_sound.stop()
                    if self.__answer_index__(event.key, self.rand) == self.rand:
                        self.temp_property = 1
                        self.end_answer_time = time.time()
                        self.correct_sound.play()
                        self.answer_time_list.append(self.end_answer_time - self.start_answer_time)
                    else:
                        self.temp_property = 2
                        self.wrong_sound.play()
                    self.start_property_time = time.time()      

    def __answer_index__(self, key, rand):
        if rand >= 0 and rand <= 3:
            return self.answer_green_list.index(key)

        elif rand >= 4 and rand <= 7:
            return self.answer_red_list.index(key) + 4

    def __update_roles__(self):
        
        self.screen.fill("#808080")
        self.screen.blit(self.description, (900, 0))
        self.__showquestion__()
        if self.temp_property != 0:
            # 答题后显示对号和叉号
            self.__show_temp_property__()
            self.end_property_time = time.time()
            if self.end_property_time - self.start_property_time > 1:
                if self.temp_property == 1:
                    self.correct_num += 1
                self.temp_property = 0
                self.question_num += 1
                if self.question_num <= self.question_sum:
                    self.rand = self.__randnum__()
                    self.start_answer_time = time.time()
                elif self.question_num > self.question_sum:
                    self.arrange_answer_time = sum(self.answer_time_list) / len(self.answer_time_list)
                    result = Result(self.question_sum, self.correct_num, self.arrange_answer_time)
                    result.startGame()

        self.__showscore__()

    def __showquestion__(self):
        # 显示问题
        self.screen.blit(self.question_list[self.rand], (0, 0))

    def __show_temp_property__(self):
        # 答题后显示对号和叉号
        if self.temp_property == 1:
            self.screen.blit(pygame.image.load("images/right.png"), (300, 300))
        elif self.temp_property == 2:
            self.screen.blit(pygame.image.load("images/wrong.png"), (300, 300))

    def __showscore__(self):
        # 显示正确题数和已做题数
            self.screen.blit(pygame.image.load("images/questionnum.png").convert_alpha(), (0, 0))
            self.screen.blit(pygame.image.load("images/correctnum.png").convert_alpha(), (740, 0))
            self.screen.blit(pygame.image.load("images/number.png").convert_alpha(), (170, 0))
            ques_shiwei = str(int(self.question_num // 10))
            ques_gewei = str(self.question_num % 10)
            sum_shiwei = str(int(self.question_sum // 10))
            sum_gewei = str(self.question_sum % 10)
            corr_shiwei = str(int(self.correct_num // 10))
            corr_gewei = str(self.correct_num % 10)
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
        pygame.display.set_caption("方向判断")
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
    ready = Ready()
    ready.startGame()

if __name__ == '__main__':
    main()
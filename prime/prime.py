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

class PrimeReady(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找素数")
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
            prime = Prime()
            prime.startGame()

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

class Prime(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找素数")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.clock = pygame.time.Clock()
        self.__createitems__()

        self.correctnum = 0

        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)
        

    def __createitems__(self):
        self.chessboard = Chessboard("images/chessboard.png").image
        self.chessboard_index = 5 # 显示几*几的方格
        self.difficulty_rank = [0, 1, 2]
        self.question_sum = 10 # 题目总量
        self.question_num = 1 # 当前做到第几题
        self.hoverindex = 999 # 鼠标悬停时的格子下标。也不知道怎么办就用999占位置吧，不占位置报错啊
        self.difficulty_list = self.__set_difficulty_list__() # 根据题目数量定不同数量不同难度的题目
        self.prime_number_list = [[5, 7, 11, 13, 17, 19, 23, 29], [31, 37, 41, 43, 47], [53, 59, 61, 67, 71, 73, 79, 83, 89, 97]] # 三种难度的质数表
        self.composite_number_list = [[4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30], [32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50], [51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99]] # 三种难度的合数表
        self.user_prime_number_list = [] # 保存用户当前难度下的数字表
        self.user_composite_number_list = []
        self.__setquestion__() #出题
        
        self.temp_property = 0 # 记录单题的正确与否（1对2错0未作答）
        self.start_answer_time = time.time() # 单题作答时间
        self.end_answer_time = 0
        self.answer_time_list = [] # 做题时间列表
        self.start_property_time = 0 # 显示对勾、叉号时间
        self.end_property_time = 0
        

    def __set_difficulty_list__(self):
        # 根据题目数量定不同数量不同难度的题目
        temp = []
        centerindex1 = self.question_sum // 2
        centerindex2 = centerindex1 // 2
        if centerindex2 > 0:
            for i in range(centerindex2):
                temp.append(self.difficulty_rank[0])
            for i in range(centerindex1 - centerindex2):
                temp.append(self.difficulty_rank[1])
            for i in range(self.question_sum - centerindex1):
                temp.append(self.difficulty_rank[2])
        elif centerindex2 <= 0:
            for i in range(centerindex1):
                temp.append(self.difficulty_rank[1])
            for i in range(self.question_sum - centerindex1):
                temp.append(self.difficulty_rank[2])
        return temp
    
    def __setquestion__(self):
        # 出题
        # 1.根据难度确定要画几*几的方格，并定当前题目的数字组
        if self.difficulty_list[self.question_num - 1] == 0: # self.question_num是从1开始算的，需要减1
            self.chessboard_index = 3
            self.user_prime_number_list = self.prime_number_list[0]
            self.user_composite_number_list = self.composite_number_list[0]
        elif self.difficulty_list[self.question_num - 1] == 1:
            self.chessboard_index = 4
            self.user_prime_number_list = self.prime_number_list[0] + self.prime_number_list[1]
            self.user_composite_number_list = self.composite_number_list[0] + self.composite_number_list[1]
        elif self.difficulty_list[self.question_num - 1] == 2:
            self.chessboard_index = 5
            self.user_prime_number_list = self.prime_number_list[0] + self.prime_number_list[1] + self.prime_number_list[2]
            self.user_composite_number_list = self.composite_number_list[0] + self.composite_number_list[1] + self.composite_number_list[2]
        # 2.定随机素数的位置、随机素数答案和随机合数组合
        self.temp_answer_pos = random.randint(0, (self.chessboard_index ** 2 - 1))
        temp_answer = random.choice(self.user_prime_number_list)
        temp_numlist = random.sample(self.user_composite_number_list, (self.chessboard_index ** 2 - 1)) # 随机出足量的合数，建立数字列表
        temp_numlist.insert(self.temp_answer_pos, temp_answer) # 质数占位
        # 3.把质数、合数都用NumberFont类实例化，保存在一个列表中
        self.temp_number_list = []
        for i in range(0, self.chessboard_index ** 2):
            if i == self.temp_answer_pos:
                property = "prime"
            elif i != self.temp_answer_pos:
                property = "composite"
            self.temp_number_list.append(NumberFont(temp_numlist[i], property, i, self.chessboard_index))

    def startGame(self):
        self.start_sound.play()
        while True:
            self.clock.tick(60)
            self.__eventhandler__()
            self.__update__()
            pygame.display.flip()

    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                mouseposx = mousepos[0]
                mouseposy = mousepos[1]
                mouseindex = self.__getmouseindex__(mouseposx, mouseposy)
                if mouseindex != None:
                    self.hoverindex = mouseindex
                else:
                    self.hoverindex = 999

            if event.type == pygame.MOUSEBUTTONDOWN:
                keyarr = pygame.mouse.get_pressed()
                for index in range(len(keyarr)):
                    if keyarr[index] and index == 0:
                        keypos = pygame.mouse.get_pos()
                        keyindex = self.__getmouseindex__(keypos[0], keypos[1])
                        if keyindex != None:
                            if self.temp_property == 0:
                                if self.start_sound.play():
                                    self.start_sound.stop()
                                if keyindex == self.temp_answer_pos:
                                    self.temp_property = 1
                                    self.correct_sound.play()
                                    self.end_answer_time = time.time()
                                    self.answer_time_list.append(self.end_answer_time - self.start_answer_time)
                                else:
                                    self.temp_property = 2
                                    self.wrong_sound.play()
                                self.start_property_time = time.time()                           
    
    def __getmouseindex__(self, x, y):
        res = 999
        i = int((x - ((900 - 100 * self.chessboard_index) / 2)) // 100)
        j = int((y - ((700 - 100 * self.chessboard_index) / 2)) // 100)
        if i >= 0 and j >= 0 and i < self.chessboard_index and j < self.chessboard_index:
            res = j * self.chessboard_index + i
        if res >= 0 and res < self.chessboard_index ** 2:
            return res
        else:
            return None

    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        # 显示方格
        self.__show_chessboard__()
        # 显示数字
        for i in range(len(self.temp_number_list)):
            self.screen.blit(self.temp_number_list[i].numfont, self.temp_number_list[i].rect)
        # 如鼠标悬停，显示hover图片
        if self.hoverindex >= 0 and self.hoverindex < self.chessboard_index ** 2:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/hover.png").convert_alpha(), (100, 100)), (((self.hoverindex % self.chessboard_index) * 100) + (900 - 100 * self.chessboard_index) / 2, ((self.hoverindex // self.chessboard_index) * 100) + (700 - 100 * self.chessboard_index) / 2))
        # 显示对勾或叉号 显示1秒后切到下一题
        if self.temp_property != 0:
            self.__showproperty__()
            self.end_property_time = time.time()
            if self.end_property_time - self.start_property_time > 1.0:
                if self.temp_property == 1:
                    self.correctnum += 1
                self.temp_property = 0
                if self.question_num < self.question_sum:
                    self.question_num += 1
                    self.__setquestion__()
                    self.start_answer_time = time.time()
                elif self.question_num >= self.question_sum:
                    # 首先计算平均作答时间
                    arrange = sum(self.answer_time_list) / len(self.answer_time_list)
                    result = Result(self.question_sum, self.question_num, arrange)
                    result.startGame()
                    
                
        # 显示顶部文字
        self.questionfont = self.font.render("题目数量：" + str(self.question_num) + " / " + str(self.question_sum), True, 'black')
        self.questionrect = self.questionfont.get_rect()
        self.questionrect.left = 0
        self.questionrect.top = 0
        self.correctfont = self.font.render("正确数量：" + str(self.correctnum), True, 'black')
        self.correctrect = self.correctfont.get_rect()
        self.correctrect.left = 0
        self.correctrect.right = 900
        self.screen.blit(self.questionfont, self.questionrect)
        self.screen.blit(self.correctfont, self.correctrect)

    def __show_chessboard__(self):
        for i in range(0, self.chessboard_index ** 2):
            x = i % self.chessboard_index
            y = i // self.chessboard_index
            self.screen.blit(self.chessboard, ((x * 100) + (900 - 100 * self.chessboard_index) / 2, (y * 100) + (700 - 100 * self.chessboard_index) / 2))
            
    def __showproperty__(self):
        if self.temp_property == 1:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/right.png").convert_alpha(), (150, 110)), (700, 500))
        elif self.temp_property == 2:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110)), (700, 500))

class Result(object):
    # 显示结果
    def __init__(self, sum, correctnum, arrange):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找素数")
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
                            ready = PrimeReady()
                            ready.startGame()


    def __update__(self):
        self.screen.fill("#808080")
        text1 = self.font.render("任务完成", True, (0, 0, 0))
        text2 = self.font.render("你的正确题数：" + str(self.correctnum) + "   平均作答时间：" + str(round(self.arrange, 2)) + "秒", True, (0, 0, 0))
        text3 = self.font.render("你的得分："+ str(self.score), True, (0, 0, 0))
        self.screen.blit(text1, (150, 150))
        self.screen.blit(text2, (150, 250))
        self.screen.blit(text3, (150, 350))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))


def primeGame():
    # prime = Prime()
    # prime.startGame()
    ready = PrimeReady()
    ready.startGame()

if __name__ == "__main__":
    primeGame()

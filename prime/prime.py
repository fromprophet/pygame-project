import pygame
import sys
import random
import time
from gameObject import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Prime(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.clock = pygame.time.Clock()
        self.__createitems__()

        self.correctnum = 0
        self.correct_time_list = []

    def __createitems__(self):
        self.chessboard = Chessboard("images/chessboard.png").image
        self.chessboard_index = 5 # 显示几*几的方格
        self.difficulty_rank = [0, 1, 2]
        self.question_sum = 10 # 题目总量
        self.question_num = 1 # 当前做到第几题
        self.hoverindex = 999 # 鼠标悬停时的格子下标。也不知道怎么办就用999占位置吧，不占位置报错啊
        self.difficulty_list = self.__set_difficulty_list__() # 根据题目数量定不同数量不同难度的题目
        self.prime_number_list = [[5, 7, 11, 13, 17, 19, 23, 29], [31, 37, 41, 43, 47], [53, 59, 61, 67, 71, 73, 79, 83, 89, 97]] # 三种难度的质数表
        self.composite_number_list = [[4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30], [32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50], [51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]] # 三种难度的合数表
        self.user_prime_number_list = [] # 保存用户当前难度下的数字表
        self.user_composite_number_list = []
        self.__setquestion__() #出题

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
                            if keyindex == self.temp_answer_pos:
                                self.correctnum += 1
                            else:
                                print("false")
                            self.question_num += 1
                            self.__setquestion__()
    
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
        # 显示对勾或叉号
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

def primeGame():
    prime = Prime()
    prime.startGame()

if __name__ == "__main__":
    primeGame()

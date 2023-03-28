import pygame
import sys
import random
from gameObject import *
from gamePart import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Genie(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        self.level = 1 # 难度
        self.property_list = ["黄色", "棕色", "蓝色", "红色", "绿色"]

        self.mode = "memory" # 控制做题阶段。 memory：记忆阶段 select：选择阶段
        self.__createroles__()
        
    def __createroles__(self):
        # spriteNum = self.level + 1 # 每个难度下显示精灵的种数
        # self.temp_index_list = self.property_list[0:self.level + 1] # 用切片的形式保存当前难度下精灵种类
        self.temp_random_index = random.randint(0, self.level) # 随机该题答案
        self.index_list = [] # 保存所有精灵的index
        self.sprite_list = [] # 保存所有SpriteItem类
        
        self.index_list = self.__set_index_list__()
        flag = self.__judge_index_correction__()
        print(self.temp_random_index, self.index_list, flag)
        # 如果答案种类精灵的个数不够，说明题出的不合理，需要重新出题
        while flag == False:
            self.index_list = self.__set_index_list__()
            flag = self.__judge_index_correction__()
        print(self.temp_random_index, self.index_list, flag)
        # 判断出题合理后，给所有精灵赋值
        self.sprite_list = self.__set_sprite_list__()
        
        # 题出完了给两个gamePart的类赋值
        self.memory = Memory(self.screen, self.sprite_list, self.level)
        self.select = Select(self.screen, self.sprite_list, self.level, self.temp_random_index)
        
    def __set_index_list__(self):
        # 随机所有精灵的种类，返回下标数组
        templis = []
        for i in range(self.level):
            row = []
            for j in range(9): # 最多有4行，一行最多9个
                tempindex = random.randint(0, self.level)
                row.append(tempindex)
            templis.append(row)
        return templis
                
    def __judge_index_correction__(self):
        # 判断随机题目的正确性。正确条件为：答案种类精灵的个数足够
        count = 0
        for i in range(len(self.index_list)):
            for j in range(len(self.index_list[i])):
                if self.index_list[i][j] == self.temp_random_index:
                    count += 1
        if count > self.level:
            return True
        elif count <= self.level:
            return False
    
    def __set_sprite_list__(self):
        templis = []
        for i in range(self.level):
            row = []
            for j in range(9):
                index = self.index_list[i][j]
                spriteitem = SpriteItem(self.screen, index)
                spriteitem.property = 1 # 默认显示正面
                spriteitem.listindex = [i, j]
                row.append(spriteitem)
            templis.append(row)
        return templis
                
        
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
            if self.mode == "memory":
                self.memory.eventhandler(event)
                
            if self.memory.mode == "select":
                self.mode = "select"
                self.__turnover__()
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        if self.memory.mode == "select":
            self.mode = "select" # 因为切到select界面有鼠标操作和倒计时两种方法，所以需要写两次。这里不写切界面会有延迟
            self.__turnover__()
            
        if self.mode == "memory":
            self.memory.update()
        elif self.mode == "select":
            self.select.update()
        
    def __turnover__(self):
        # 所有的精灵全部翻面
        # 注：该方法不能写在Select类的构造函数中
        for i in range(len(self.sprite_list)):
            for j in range(len(self.sprite_list[i])):
                self.sprite_list[i][j].property = 2
        
def genieGame():
    genie = Genie()
    genie.startGame()
    
if __name__ == "__main__":
    genieGame()
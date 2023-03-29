import pygame
import sys
import random
import math
import time
from gameObject import *
from gamePart import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class GenieReady(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找精灵")
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
            genie = Genie()
            genie.startGame()

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

class Genie(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找精灵")
        self.clock = pygame.time.Clock()
        self.level = 1 # 难度
        self.property_list = ["黄色", "棕色", "蓝色", "红色", "绿色"]

        self.mode = "memory" # 控制做题阶段。 memory：记忆阶段 select：选择阶段
        self.__createroles__()
        
    def __createroles__(self):
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
            if self.memory.mode == "select":
                self.mode = "select"
                self.__turnover__()
                self.memory.mode = "memory" # 这里把Memory类的mode属性改回去，以避免重复判断
            if self.select.mode == "memory":
                self.mode = "memory"
                self.select.mode = "select"
                self.level += 1
                self.__createroles__() # 出新题    
                
            if self.select.iscomplete != 0:
                if self.select.iscomplete == 1:
                    result = Result(self.level, True) # 已通关
                elif self.select.iscomplete == 2:
                    result = Result(self.level, False) # 未通关
                self.select.iscomplete = 0
                result.startGame() # 对于是否进入result界面的判断需要放在game类不能放在别的文件，否则将引起两个文件互相导引发死锁，程序闪退
                
            if self.mode == "memory":
                self.memory.eventhandler(event)
            if self.mode == "select":
                self.select.eventhandler(event)
                
            
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        if self.memory.mode == "select":
            self.mode = "select" # 因为切到select界面有鼠标操作和倒计时两种方法，所以需要写两次。这里不写切界面会有延迟
            self.__turnover__()
            self.memory.mode = "memory" # 这里把Memory类的mode属性改回去，以避免重复判断
            
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
                
class Result(object):
    # 显示结果
    def __init__(self, level, iscomplete):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("找精灵")
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 48)
        self.sum = sum
        self.level = level
        self.iscomplete = iscomplete # 是否通关
        self.__setfonts__()
        
    def __setfonts__(self):
        if self.iscomplete == True:
            self.text1 = self.font.render("恭喜通关！", True, (0, 0, 0))
            self.text2 = self.font.render("已完成所有难度", True, (0, 0, 0))
        elif self.iscomplete == False:
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
                            ready = GenieReady()
                            ready.startGame()

    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(self.text1, (150, 150))
        self.screen.blit(self.text2, (150, 250))
        self.screen.blit(pygame.image.load("images/restart.png").convert_alpha(), (500, 450))

        
def genieGame():
    # genie = Genie()
    # genie.startGame()
    ready = GenieReady()
    ready.startGame()
    
if __name__ == "__main__":
    genieGame()
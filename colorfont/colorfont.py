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

class ColorfontReady(object):
    # 准备界面
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("颜色？文字？")
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
            colorfont = ColorFont()
            colorfont.startGame()

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

class ColorFont(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("颜色？文字？")
        self.clock = pygame.time.Clock()
        self.font = self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.question_sum = 10
        self.question_num = 1
        self.correctnum = 0
        
        self.fontlist = ["黑色", "白色", "红色", "绿色", "蓝色", "黄色", "粉色"]
        self.colorlist = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
        self.propertylist = ["文字", "颜色"]

        self.start_sound = pygame.mixer.Sound("sounds/start.mp3")
        self.start_sound.set_volume(0.3)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)

        self.__createroles__()
        
        self.motionindex = None
        self.temp_property = 0 # 记录单题的正确与否（1对2错0未作答）
        self.start_answer_time = time.time() # 单题作答时间
        self.end_answer_time = 0
        self.answer_time_list = [] # 做题时间列表
        self.start_property_time = 0 # 显示对勾、叉号时间
        self.end_property_time = 0
        
    def __createroles__(self):
        self.__setquestion__()
        
    def __setquestion__(self):
        # 出题
        self.answer_list = [] # 保存单题中四个选项
        self.__setstem__()
        self.__setoption__()
        
    def __setstem__(self):
        # 设置题干
        self.questionfont = Character(random.choice(self.fontlist), random.choice(self.colorlist))
        self.questionfont.rect.x = 215
        self.questionfont.rect.y = 200
        
        self.propertyfont = Character(random.choice(self.propertylist), 'black')
        self.propertyfont.rect.x = 400
        self.propertyfont.rect.y = 200
        
    def __setoption__(self):
        # 设置选项
        # 首先随机正确答案
        self.tempanswer = random.randint(0, 3)
        f = self.questionfont.fontname # 答案 文字
        c = self.questionfont.color # 答案 颜色
        p = self.propertyfont.fontname # 答案 属性
        
        tempfont = ""
        tempcolor = ""
        # 4个选项
        for i in range(0, 4):
            if i != self.tempanswer:
                if p == "文字":
                    tempfont = self.__setrandomitem__(f, self.fontlist)
                    tempcolor = random.choice(self.colorlist)
                elif p == "颜色":
                    tempfont = random.choice(self.fontlist)
                    tempcolor = self.__setrandomitem__(c, self.colorlist)
            elif i == self.tempanswer:
                if p == "文字":
                    tempfont = f
                    tempcolor = random.choice(self.colorlist)
                elif p == "颜色":
                    tempfont = random.choice(self.fontlist)
                    tempcolor = c
            temptext = Character(tempfont, tempcolor)
            temptext.rect.width = 150
            temptext.rect.height = 100
            temptext.rect.centerx = 150 * i + 170 + i * 30
            temptext.rect.centery = 430
            self.answer_list.append(temptext)
                
    def __setrandomitem__(self, property, lis):
        # 设置答案时，非正确选项的属性在随机时需要规避掉正确答案。另一个属性随便即可
        res = random.choice(lis)
        if res != property:
            return res
        elif res == property:
            return self.__setrandomitem__(property, lis) # 如果随机的相同，就递归重新随机
        
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
                self.motionindex = self.__getmouseindex__(mouseposx, mouseposy)
            if event.type == pygame.MOUSEBUTTONDOWN:
                keyarr = pygame.mouse.get_pressed()
                for index in range(len(keyarr)):
                    if keyarr[index] and index == 0:
                        keypos = pygame.mouse.get_pos()
                        keyindex = self.__getmouseindex__(keypos[0], keypos[1])
                        if keyindex != None and self.temp_property == 0:
                            if self.start_sound.play():
                                self.start_sound.stop()
                            if keyindex == self.tempanswer:
                                self.temp_property = 1
                                self.correct_sound.play()
                                self.end_answer_time = time.time()
                                self.answer_time_list.append(self.end_answer_time - self.start_answer_time)
                            elif keyindex != self.tempanswer:
                                self.temp_property = 2
                                self.wrong_sound.play()
                            self.start_property_time = time.time()
                     
    def __getmouseindex__(self, x, y):
        # 获取鼠标在哪个选项上
        if y > 350 and y < 450:
            if x > 50 and x < 200:
                return 0
            elif x > 230 and x < 380:
                return 1
            elif x > 410 and x < 560:
                return 2
            elif x > 590 and x < 740:
                return 3
            else:
                return None
        else:
            return None
                
    def __update__(self):
        self.screen.fill("#808080")
        # 显示description
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        
        # 显示问题文字及属性文字
        self.screen.blit(self.questionfont.text, self.questionfont.rect)
        self.screen.blit(self.propertyfont.text, self.propertyfont.rect)
        # 显示4个选项框
        for i in range(4):
            pygame.draw.rect(self.screen, 'black', ((150 * i + 50 + i * 30), 350, 150, 100), width = 1)
        # 显示4个选项
        for i in range(len(self.answer_list)):
            self.screen.blit(self.answer_list[i].text, self.answer_list[i].rect)
        # 鼠标悬停显示hover
        if self.motionindex != None:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/hover.png").convert_alpha(), (150, 100)), ((150 * self.motionindex + 50 + self.motionindex * 30), 350))
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
                    
        # 显示文字
        self.description = self.font.render(str(self.question_num) + ".请选择       的", True, 'black')
        self.description_rect = self.description.get_rect()
        self.description_rect.x = 50
        self.description_rect.y = 200
        self.screen.blit(self.description, self.description_rect)# 显示题干文字
        self.font1 = self.font.render("题目数量：" + str(self.question_num) + " / " + str(self.question_sum), True, 'black')
        self.rect1 = self.font1.get_rect()
        self.rect1.left = 0
        self.rect1.top = 0
        self.correctfont = self.font.render("正确数量：" + str(self.correctnum), True, 'black')
        self.correctrect = self.correctfont.get_rect()
        self.correctrect.left = 0
        self.correctrect.right = 900
        self.screen.blit(self.font1, self.rect1)
        self.screen.blit(self.correctfont, self.correctrect)
        
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
        pygame.display.set_caption("颜色？文字？")
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
                            ready = ColorfontReady()
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
    
def colorfontGame():
    # colorfont = ColorFont()
    # colorfont.startGame()
    colorfontReady = ColorfontReady()
    colorfontReady.startGame()
    
if __name__ == "__main__":
    colorfontGame()
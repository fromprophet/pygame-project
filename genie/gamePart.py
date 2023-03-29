import pygame
import time
from gameObject import *

class Memory(object):
    def __init__(self, screen, sprite_list, level):
        super().__init__()
        self.screen = screen
        self.sprite_list = sprite_list
        self.level = level
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.chessboard = Chessboard("images/chessboard.png").image
        self.mode = "memory" # 控制做题阶段。 memory：记忆阶段 select：选择阶段
        
        self.descriptionfont = self.font.render("第一阶段：请记住以下所有精灵及位置", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 100
        
        self.start_countdown = time.time() # 倒计时
        self.end_countdown = time.time()
        
    def eventhandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            keyarr = pygame.mouse.get_pressed()
            for index in range(len(keyarr)):
                if keyarr[index] and index == 0:
                    keypos = pygame.mouse.get_pos()
                    keyposx = keypos[0]
                    keyposy = keypos[1]
                    if keyposx > 370 and keyposx < 530 and keyposy > 580 and keyposy < 660:
                        self.start_countdown = 0
                        self.end_countdown = 0 # 停止倒计时
                        self.mode = "select"
    
    def update(self):
        # 显示精灵
        if len(self.sprite_list) != 0:
            for i in range(len(self.sprite_list)):
                for j in range(len(self.sprite_list[i])):
                    self.screen.blit(self.chessboard, ((j * 80 + 90), (i * 80 + 150))) # 显示棋盘
                    self.sprite_list[i][j].show()
        # 显示标题文字
        self.screen.blit(self.descriptionfont, self.descriptionrect)
        self.levelfont = self.font.render("当前难度：" + str(self.level), True, 'black')
        self.levelrect = self.levelfont.get_rect()
        self.levelrect.right = 900
        self.levelrect.top = 0
        self.screen.blit(self.levelfont, self.levelrect)
        # 显示“我记住了”按钮
        self.screen.blit(pygame.transform.scale(pygame.image.load("images/memory.png").convert_alpha(), (160, 80)), (370, 580))
        # 显示倒计时
        self.end_countdown = time.time()
        self.countdown = round((5.0 * self.level) - (self.end_countdown - self.start_countdown), 2)
        if self.countdown <= 0.0:
            self.start_countdown = 0
            self.end_countdown = 0 # 停止倒计时
            self.mode = "select"
        else:
            self.__showcountdown__()
        
    def __showcountdown__(self):
        # 显示倒计时      
        # 倒计时文字
        self.countdownfont = self.font.render("倒计时：" + str(self.countdown), True, 'black')
        self.countdownrect = self.countdownfont.get_rect()
        self.countdownrect.left = 0
        self.countdownrect.top = 0
        self.screen.blit(self.countdownfont, self.countdownrect)
        # 倒计时进度指示
        percentage = self.countdown / (5.0 * self.level)
        pygame.draw.line(self.screen, 'red', (250, 18), ((250 + percentage * 400), 18), width = 5)
        pygame.draw.rect(self.screen, 'black', (248, 13, 400, 10), width = 2)
        
class Select(object):
    def __init__(self, screen, sprite_list, level, temp_random_index):
        super().__init__()
        self.screen = screen
        self.sprite_list = sprite_list
        self.level = level
        self.temp_random_index = temp_random_index # 该题所需要的精灵种类
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.chessboard = Chessboard("images/chessboard.png").image
        self.mode = "select" # 控制做题阶段。 memory：记忆阶段 select：选择阶段
        self.mouseindex = None # 控制当前鼠标放在哪个格子上，默认设为None
        self.temp_property = 0 # 记录单题的正确与否（1对2错0未作答）
        self.iscomplete = 0 # 记录是否通关（1已通关2未通关）
        self.clickmode = "none" # 存储点击按钮情况 none无按钮 nextlevel下一题 result进入结算
        self.playeranswerlist = [] # 记录用户单题作答情况
        self.wronganswerlist = [] # 如用户点错了把下标放在此列表中
        
        self.__createroles__()
        
    def __createroles__(self):
        self.property_list = ["黄色", "棕色", "蓝色", "红色", "绿色"]
        self.temp_property_list = self.property_list[0:self.level + 1] # 用切片的形式保存当前难度下精灵种类
        
        self.descriptionfont = self.font.render("第二阶段：请选择" + str(self.level) + "个  " + self.temp_property_list[self.temp_random_index] + "  精灵      的位置", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 100
        
        # 创建一个SpriteItem对象，放在题干处
        self.tempsprite = SpriteItem(self.screen, self.temp_random_index)
        
    def eventhandler(self, event):
        if event.type == pygame.MOUSEMOTION:
            motionpos = pygame.mouse.get_pos()
            posx = motionpos[0]
            posy = motionpos[1]
            self.mouseindex = self.__getmouseindex__(posx, posy)
        if event.type == pygame.MOUSEBUTTONDOWN:
            keyarr = pygame.mouse.get_pressed()
            for index in range(len(keyarr)):
                if keyarr[index] and index == 0:
                    keypos = pygame.mouse.get_pos()
                    keyposx = keypos[0]
                    keyposy = keypos[1]
                    if keyposx > 370 and keyposx < 530 and keyposy > 580 and keyposy < 660:
                        if self.clickmode == "nextlevel":
                            self.mode = "memory"
                        elif self.clickmode == "result":
                            if self.temp_property == 1:
                                self.iscomplete = 1
                            elif self.temp_property == 2:
                                self.iscomplete = 2
                    else:
                        keyindex = self.__getmouseindex__(keyposx, keyposy)
                        if keyindex != None and self.temp_property == 0 and len(self.playeranswerlist) < self.level:
                                if self.sprite_list[keyindex[0]][keyindex[1]].property == 2:
                                    self.sprite_list[keyindex[0]][keyindex[1]].property = 1 # 将用户点击的方块翻面
                                    if self.sprite_list[keyindex[0]][keyindex[1]].index == self.temp_random_index:
                                        # 如用户点对了(已翻面的不能再次翻面)
                                        self.playeranswerlist.append([keyindex[0], keyindex[1]])
                                        if len(self.playeranswerlist) == self.level:
                                            self.temp_property = 1
                                    elif self.sprite_list[keyindex[0]][keyindex[1]].index != self.temp_random_index:
                                        # 如用户点错了
                                        self.wronganswerlist.append([keyindex[0], keyindex[1]])
                                        self.temp_property = 2
                    
            
    def __getmouseindex__(self, x, y):
        # 获取当前鼠标在哪个格子上。
        res = []
        i = (y - 150) // 80
        j = (x - 90) // 80
        if i >= 0 and j >= 0 and i < self.level and j < 9:
            res = [i, j]
        if len(res) != 0:
            return res
        else:
            return None
    
    def update(self):
        # 显示精灵
        if len(self.sprite_list) != 0:
            for i in range(len(self.sprite_list)):
                for j in range(len(self.sprite_list[i])):
                    self.screen.blit(self.chessboard, ((j * 80 + 90), (i * 80 + 150))) # 显示棋盘
                    self.sprite_list[i][j].show()
        # 显示标题文字
        self.screen.blit(self.descriptionfont, self.descriptionrect)
        self.levelfont = self.font.render("当前难度：" + str(self.level), True, 'black')
        self.levelrect = self.levelfont.get_rect()
        self.levelrect.right = 900
        self.levelrect.top = 0
        self.screen.blit(self.levelfont, self.levelrect)
        self.screen.blit(self.tempsprite.image1, (620, 60))
        # 显示hover
        if self.mouseindex != None and self.sprite_list[self.mouseindex[0]][self.mouseindex[1]].property == 2: # 写and后面的条件为了避免翻面后还是显示hover
            self.screen.blit(pygame.image.load("images/hover.png").convert_alpha(), ((self.mouseindex[1] * 80 + 90), (self.mouseindex[0] * 80 + 150)))
        # 显示绿框或红框
        if len(self.playeranswerlist) != 0:
            for i in range(len(self.playeranswerlist)):
                pygame.draw.rect(self.screen, "green", ((self.playeranswerlist[i][1] * 80 + 90), (self.playeranswerlist[i][0] * 80 + 150), 80, 80), width = 3)
        if len(self.wronganswerlist) != 0:
            for i in range(len(self.wronganswerlist)):
                pygame.draw.rect(self.screen, "red", ((self.wronganswerlist[i][1] * 80 + 90), (self.wronganswerlist[i][0] * 80 + 150), 80, 80), width = 3)
        # 显示对勾或叉号
        if self.temp_property == 1:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/right.png").convert_alpha(), (150, 110)), (700, 500))
            if self.level < 4:
                self.screen.blit(pygame.transform.scale(pygame.image.load("images/nextlevel.png").convert_alpha(), (160, 80)), (370, 580))
                self.clickmode = "nextlevel"
            else:
                self.screen.blit(pygame.transform.scale(pygame.image.load("images/result.png").convert_alpha(), (160, 80)), (370, 580))
                self.clickmode = "result"
        elif self.temp_property == 2:
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110)), (700, 500))
            self.screen.blit(pygame.transform.scale(pygame.image.load("images/result.png").convert_alpha(), (160, 80)), (370, 580))
            self.clickmode = "result"
            

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
        
        self.__createroles__()
        
    def __createroles__(self):
        self.property_list = ["黄色", "棕色", "蓝色", "红色", "绿色"]
        self.temp_property_list = self.property_list[0:self.level + 1] # 用切片的形式保存当前难度下精灵种类
        print(self.temp_property_list)
        
        self.descriptionfont = self.font.render("第二阶段：请选择" + str(self.level) + "个  " + self.temp_property_list[self.temp_random_index] + "  精灵      的位置", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 100
        
        # 创建一个SpriteItem对象，放在题干处
        self.tempsprite = SpriteItem(self.screen, self.temp_random_index)
        
    def eventhandler(self):
        pass
    
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
import pygame
import time
import random
from gameObject import *

# 保存单题游戏的三个阶段：记忆阶段、选择阶段、展示结果阶段。

class Memory(object):
    # 记忆阶段
    def __init__(self, screen, chessboard_index, mirrorcount, randommirrorpos):
        super().__init__()
        self.screen = screen
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.mouse_sound = pygame.mixer.Sound("sounds/mouse.mp3")
        self.mouse_sound.set_volume(0.8)
        self.mode = "memory" # 控制单题游戏阶段。memory记忆阶段 select选择做题阶段 showresult展示结果阶段
        self.chessboard_index = chessboard_index # 控制产生几*几的棋盘
        self.mirrorcount =  mirrorcount # 随机镜子个数
        self.randommirrorpos = randommirrorpos # 随机镜子位置 得到下标列表
        self.__createbasicroles__()
        
    def __createbasicroles__(self):
        # 棋盘和镜子生成
        self.chessboard = ChessBoard("images/chessboard.png").image
        self.reflectlist = []
        for i in range(self.mirrorcount):
            reflect = Reflect(random.randint(1, 2), self.randommirrorpos[i]) # 生成“镜子”对象
            reflect.rect.topleft = [(self.randommirrorpos[i] % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (self.randommirrorpos[i] // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2] # 得到镜子的坐标
            self.reflectlist.append(reflect)
        
        # 描述文字
        self.descriptionfont = self.font.render("请记住以下镜面位置及角度", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 50
        
    def eventhandler(self, event):
        # 记忆阶段：点“我记住了”按钮后进入选择阶段
        if event.type == pygame.MOUSEBUTTONDOWN:
            keyarr = pygame.mouse.get_pressed()
            for index in range(len(keyarr)):
                if keyarr[index] and index == 0:
                    keypos = pygame.mouse.get_pos()
                    keyposx = keypos[0]
                    keyposy = keypos[1]
                    if keyposx > 350 and keyposx < 550 and keyposy > 680 and keyposy < 780:
                        self.mouse_sound.play()
                        self.mode = "select"
    
    def updateroles(self):
        # 显示棋盘、镜子以及“我记住了”按钮
        # 显示说明文字
        self.screen.blit(self.descriptionfont, self.descriptionrect)
        # 显示棋盘
        for i in range(0, self.chessboard_index ** 2):
            self.screen.blit(self.chessboard, ((i % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (i // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2))
        # 显示镜子
        for i in range(len(self.randommirrorpos)):
            self.screen.blit(self.reflectlist[i].image, self.reflectlist[i].rect)
        # 显示“我记住了”按钮
        self.screen.blit(pygame.image.load("images/memory.png").convert_alpha(), (350, 680))
        
class Select(object):
    def __init__(self, screen, chessboard_index, randommirrorpos):
        super().__init__()
        self.screen = screen
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.mouse_sound = pygame.mixer.Sound("sounds/mouse.mp3")
        self.mouse_sound.set_volume(0.8)
        self.mode = "select" # 控制单题游戏阶段。memory记忆阶段 select选择做题阶段 showresult展示结果阶段
        self.chessboard_index = chessboard_index
        self.randommirrorpos = randommirrorpos
        self.__createbasicroles__()
        
        self.randbuttonindexX, self.randbuttonindexY = self.__setbuttonindex__()
        self.buttonlist = []
        self.buttonGroup = pygame.sprite.Group() # 按钮精灵组
        self.flashGroup = pygame.sprite.Group() # 手电筒精灵组 二者分离开以便做按钮和光束的碰撞
        self.__createbutton__()
        
    def __createbasicroles__(self):
        # 棋盘和按钮生成
        self.chessboard = ChessBoard("images/chessboard.png").image
        
        self.hoverindex = [] # hover图片的下标
        self.playeranswer = [] # 如用户点击了按钮，保存结果[方向，个数]
        
        # 描述文字
        self.descriptionfont = self.font.render("选择光线出射点", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 30
    
    def __setbuttonindex__(self):
        # 随机生成手电筒位置
        randbuttonindexX = random.randint(0, 3)
        randbuttonindexY = random.randint(0, self.chessboard_index - 1)
        flag = self.__judgebuttonindex__(randbuttonindexX, randbuttonindexY)
        while flag == True:
            randbuttonindexX = random.randint(0, 3)
            randbuttonindexY = random.randint(0, self.chessboard_index - 1)
            flag = self.__judgebuttonindex__(randbuttonindexX, randbuttonindexY)
        return randbuttonindexX, randbuttonindexY
    
    def __judgebuttonindex__(self, x, y):
        # 手电筒随机后进行判断，如果没有经过任何镜面，就需要再次进行一次随机。换言之如果经过了一次镜面就无需再次随机
        # x：上下左右 y:第几个 x = 0 or x = 1:找列  x = 2 or x = 3 找行
        flag = True
        for i in range(len(self.randommirrorpos)):
            if x == 0 or x == 1:
                if self.randommirrorpos[i] % self.chessboard_index == y:
                    flag = False
                    break
            elif x == 2 or x == 3:
                if self.randommirrorpos[i] // self.chessboard_index == y:
                    flag = False
                    break
        return flag
        
    def __createbutton__(self):
        # 创建按钮
        for i in range(0, 4):
            temp = []
            for j in range(0, self.chessboard_index):
                button = Button("button", i, True)
                if i == self.randbuttonindexX and j == self.randbuttonindexY:
                    button = Button("flash", i, True)
                if i >= 0 and i <= 1:
                    button.rect.x = (j % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2
                    button.rect.y = (i % 2) * (100 * (self.chessboard_index + 1)) + (800 - 100 * (self.chessboard_index + 2)) / 2
                elif i >= 2 and i <= 3:
                    button.rect.x = (i % 2) * (100 * (self.chessboard_index + 1)) + (900 - 100 * (self.chessboard_index + 2)) / 2
                    button.rect.y = (j % self.chessboard_index) * 100 + (800 - 100 * self.chessboard_index) / 2
                
                button.indexposition = [i, j]
                temp.append(button)
            self.buttonlist.append(temp)
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if self.buttonlist[i][j].property == "button":
                    self.buttonGroup.add(self.buttonlist[i][j])
                elif self.buttonlist[i][j].property == "flash":
                    self.flashGroup.add(self.buttonlist[i][j])
                    
    def eventhandler(self, event):
        if event.type == pygame.MOUSEMOTION:
            motionpos = pygame.mouse.get_pos()
            motionposx = motionpos[0]
            motionposy = motionpos[1]
            temp = self.__get_button_index__(motionposx, motionposy)
            if temp != None:
                self.hoverindex = temp.indexposition
            elif temp == None:
                self.hoverindex = []
        elif event.type == pygame.MOUSEBUTTONDOWN:
            keyarr = pygame.mouse.get_pressed()
            for index in range(len(keyarr)):
                if keyarr[index] and index == 0:
                    keypos = pygame.mouse.get_pos()
                    keyposx = keypos[0]
                    keyposy = keypos[1]
                    temp = self.__get_button_index__(keyposx, keyposy)
                    if temp == None:
                        self.playeranswer = []
                    elif temp != None:
                        self.playeranswer = temp.indexposition # 得到用户答案
                        self.mouse_sound.play()
                        self.mode = "showresult"
    
    def __get_button_index__(self, x, y):
        # 根据鼠标位置找到鼠标在哪个按钮上，并返回这个按钮对象
        temp = None
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if x > self.buttonlist[i][j].rect.topleft[0] and x < self.buttonlist[i][j].rect.topright[0] and y > self.buttonlist[i][j].rect.topleft[1] and y < self.buttonlist[i][j].rect.bottomleft[1]: # 最后的判定条件是为了不点击
                    temp = self.buttonlist[i][j]
        return temp
                
        
    def updateroles(self):
        # 显示棋盘、按钮
        # 显示棋盘
        self.screen.blit(self.descriptionfont, self.descriptionrect)
        for i in range(0, self.chessboard_index ** 2):
            self.screen.blit(self.chessboard, ((i % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (i // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2))
        
        # 显示按钮和手电筒    
        for group in [self.buttonGroup, self.flashGroup]:
            group.draw(self.screen)
            
        # 显示hover图片（如鼠标放在上面）
        if len(self.hoverindex) != 0:
            if self.buttonlist[self.hoverindex[0]][self.hoverindex[1]].property == "button":
                if self.hoverindex[0] == 0 or self.hoverindex[0] == 1:
                    self.screen.blit(pygame.image.load("images/hover.png").convert_alpha(), ((self.hoverindex[1] % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (self.hoverindex[0] % 2) * (100 * (self.chessboard_index + 1)) + (800 - 100 * (self.chessboard_index + 2)) / 2))
                elif self.hoverindex[0] == 2 or self.hoverindex[0] == 3:
                    self.screen.blit(pygame.image.load("images/hover.png").convert_alpha(), ((self.hoverindex[0] % 2) * (100 * (self.chessboard_index + 1)) + (900 - 100 * (self.chessboard_index + 2)) / 2, (self.hoverindex[1] % self.chessboard_index) * 100 + (800 - 100 * self.chessboard_index) / 2))
                    
class Showresult(object):
    def  __init__(self, screen, chessboard_index, randommirrorpos, reflectlist = [], buttonlist = [], playeranswer = [], buttonGroup = pygame.sprite.Group(), flashGroup = pygame.sprite.Group()):
        super().__init__()
        self.screen = screen
        self.mode = "select" # 控制单题游戏阶段。memory记忆阶段 select选择做题阶段 showresult展示结果阶段
        self.changemodeflag = False # 控制是否需要切到下一题
        self.font = pygame.font.Font("fonts/国潮招牌字体.ttf", 36)
        self.correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
        self.correct_sound.set_volume(0.4)
        self.wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.wrong_sound.set_volume(0.1)
        self.chessboard_index = chessboard_index
        self.randommirrorpos = randommirrorpos
        self.reflectlist = reflectlist
        self.buttonlist = buttonlist
        self.playeranswer = playeranswer
        self.buttonGroup = buttonGroup
        self.flashGroup = flashGroup

        self.tempGroup = pygame.sprite.Group() # 把按钮和手电筒放一起（有可能出射点是手电筒）
        for i in range(len(self.buttonGroup.sprites())):
            self.tempGroup.add(self.buttonGroup.sprites()[i])
        for i in range(len(self.flashGroup.sprites())):
            self.tempGroup.add(self.flashGroup.sprites()[i])

        self.realanswer = [] # 最后得到的实际的答案
        self.playerflag = 0 # 最后作答是否正确。0：未作答 1：正确 2：错误

        self.start_property_time = 0 # 控制显示对勾和叉号的时间
        self.end_property_time = 0
        
        self.__createbasicroles__()
        
        self.lightGroup = pygame.sprite.Group()
        self.__createlight__()
        
    def __createbasicroles__(self):
        self.chessboard = ChessBoard("images/chessboard.png").image
        
        self.descriptionfont = self.font.render("显示结果", True, 'black')
        self.descriptionrect = self.descriptionfont.get_rect()
        self.descriptionrect.centerx = 450
        self.descriptionrect.centery = 30
        
    def __createlight__(self):
        # 创建光束及找到初始位置
        self.light = Light(self.flashGroup.sprites()[0].index, 10)
        # 接下来找到手电筒的下标
        for i in range(len(self.buttonlist)):
            for j in range(len(self.buttonlist[i])):
                if self.buttonlist[i][j].property == "flash":
                    rect = self.buttonlist[i][j].rect
                    break
        if self.light.index == 0:
            self.light.rect.centerx = rect.centerx
            self.light.rect.centery = rect.centery + 60
        elif self.light.index == 1:
            self.light.rect.centerx = rect.centerx
            self.light.rect.centery = rect.centery - 60
        elif self.light.index == 2:
            self.light.rect.centerx = rect.centerx + 60
            self.light.rect.centery = rect.centery
        elif self.light.index == 3:
            self.light.rect.centerx = rect.centerx - 60
            self.light.rect.centery = rect.centery
            
        self.lightGroup.add(self.light)
        self.lightpointlist = [] # 存储光线（多条直线）坐标
        self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery]) # 画光线。给出初始坐标
        
    def updateroles(self):
        self.screen.blit(self.descriptionfont, self.descriptionrect)
        # 显示棋盘
        for i in range(0, self.chessboard_index ** 2):
            self.screen.blit(self.chessboard, ((i % self.chessboard_index) * 100 + (900 - 100 * self.chessboard_index) / 2, (i // self.chessboard_index) * 100 + (800 - self.chessboard_index * 100) / 2))
            
        # 显示镜面
        for i in range(len(self.randommirrorpos)):
            self.screen.blit(self.reflectlist[i].image, self.reflectlist[i].rect)
        
        # 光线sprite移动及画线
        self.__update_light_index__()
            
        # 光线打中任何按钮前，只显示手电筒
        for group in [self.buttonGroup, self.flashGroup, self.lightGroup]:
            group.update()
            group.draw(self.screen) 
        
    def __update_light_index__(self):
        # 进行光的反射
        # 根据光“精灵”位置更新坐标列表，以便画光线
        if len(self.lightpointlist) == 1:
            self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery])
        elif len(self.lightpointlist) > 1:
            self.lightpointlist.pop(-1)
            self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery])
        # 首先找到光在哪个格子里
        self.lightpos = int(((self.light.rect.centery - ((800 - 100 * self.chessboard_index) / 2)) // 100) * self.chessboard_index + ((self.light.rect.centerx - ((900 - 100 * self.chessboard_index) / 2)) // 100))
        # 接下来把光和镜子中心点进行判断
        if self.lightpos in self.randommirrorpos:
            # （1）如果碰到了镜子，需要找到镜子的下标
            for i in range(len(self.reflectlist)):
                if self.lightpos == self.reflectlist[i].index:
                    temp = self.reflectlist[i]
                    break
            if self.light.rect.centerx == temp.rect.centerx and self.light.rect.centery == temp.rect.centery:
                # （2） 判断方向及属性，改变光的index
                if self.light.index == 0: # 从上向下射
                    if temp.property == 1:
                        self.light.index = 3
                    elif temp.property == 2:
                        self.light.index = 2
                elif self.light.index == 1: # 从下向上射
                    if temp.property == 1:
                        self.light.index = 2
                    elif temp.property == 2:
                        self.light.index = 3
                elif self.light.index == 2: # 从左向右射
                    if temp.property == 1:
                        self.light.index = 1
                    elif temp.property == 2:
                        self.light.index = 0
                elif self.light.index == 3: # 从右向左射
                    if temp.property == 1:
                        self.light.index = 0
                    elif temp.property == 2:
                        self.light.index = 1
                self.lightpointlist.append([self.light.rect.centerx, self.light.rect.centery]) # 遇到转折处打点
                
        self.__lightcollide__()
        # （3）根据光的index改方向
        self.light.directionX, self.light.directionY = self.light.setdirection()
            
        pygame.draw.lines(self.screen, 'black', False, self.lightpointlist, width = 1) # 用drawlines画光线
        
        if self.playerflag != 0:
            self.end_property_time = time.time()
            if self.end_property_time - self.start_property_time < 1.0:
                if self.playerflag == 1:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("images/right.png").convert_alpha(), (150, 110)), (410, 560))
                elif self.playerflag == 2:
                    self.screen.blit(pygame.transform.scale(pygame.image.load("images/wrong.png").convert_alpha(), (150, 110)), (410, 560))
            else:
                self.mode = "memory"
                self.changemodeflag = True # 切到下一题
        
    def __lightcollide__(self):
        # 光线和按钮碰撞检测
        collision = pygame.sprite.groupcollide(self.lightGroup, self.tempGroup, True, False) # 后两个bool值分别表示这两个精灵组如发生碰撞是否删除
        for button_sprite in collision.values():
            self.realanswer = button_sprite[0].indexposition
            if self.playerflag == 0 and len(self.realanswer) != 0 and len(self.playeranswer) != 0:
                self.start_property_time = time.time()
                if self.realanswer == self.playeranswer:
                    self.playerflag = 1
                    self.correct_sound.play()
                else:
                    self.playerflag = 2
                    self.wrong_sound.play()
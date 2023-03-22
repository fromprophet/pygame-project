import pygame
import random

class ChessBoard(object):
    # 棋盘
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
           
class Reflect(object):
    # 镜子
    def __init__(self, property):
        super().__init__()
        self.image = pygame.image.load("images/mirror" + str(property) + ".png").convert_alpha()
        
class Button(pygame.sprite.Sprite):
    # 外侧按钮
    def __init__(self, property, index, visible):
        super().__init__()
        self.property = property # 按钮属性。button:按钮 flash:手电筒
        self.index = index # 所处位置。0：上方 1：下方 2：左侧 3：右侧
        self.visible = visible # 是否可见
        self.image = pygame.image.load("images/" + str(property) + str(index) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        if visible == True:
            self.image.set_alpha(255)
        elif visible == False:
            self.image.set_alpha(0)
        
class Light(pygame.sprite.Sprite):
    # 光束
    def __init__(self, index, speed):
        super().__init__()
        self.index = index # 所处位置。0：上方 1：下方 2：左侧 3：右侧
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.directionX, self.directionY = self.__setdirection__() # 0：向下移动 1：向上移动 2：向右移动 3：向左移动
        
    def __setdirection__(self):
        x, y = 0, 0
        if self.index == 0:
            x = 0
            y = 1
        elif self.index == 1:
            x = 0
            y = -1
        elif self.index == 2:
            x = 1
            y = 0
        elif self.index == 3:
            x = -1
            y = 0
        return x, y
    
    def update(self):
        self.rect.x += self.directionX * self.speed
        self.rect.y += self.directionY * self.speed
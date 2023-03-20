import pygame
import sys
import random
import time
from gameObject import *

pygame.init()

class Finger(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        self.__createroles__()
        self.tempanswer = 0 # 保存每次答题时的答案
        self.rand = 0
        self.rand = self.__randindex__()
        
        
    def __createroles__(self):
        self.questionlist = [Question("images/finger" + str(i) + ".png").image for i in range(0, 6)]
        self.answerlist = [Answer("images/answer" + str(i) + ".png").image for i in range(0, 3)]
        self.answerlist_green = [1, 2, 3] # 1石头2剪子3布 保存答案
        self.answerlist_red = [2, 3, 1]
        
    def __randindex__(self):
        temp = random.randint(0, len(self.questionlist) - 1)
        while temp == self.rand:
            temp = random.randint(0, len(self.questionlist) - 1)
        return temp
        
    def startGame(self):
        while True:
            self.clock.tick(60)
            self.__eventHandler__()
            self.__updateRoles__()
            pygame.display.flip()
        
    def __eventHandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                indexarr = pygame.mouse.get_pressed()
                for index in range(len(indexarr)):
                    if indexarr[index] and index == 0:
                        pos = pygame.mouse.get_pos()
                        posx = pos[0]
                        posy = pos[1]
                        if posx > 150 and posx < 350 and posy > 300 and posy < 500:
                            self.tempanswer = 0
                        elif posx > 370 and posx < 570 and posy > 300 and posy < 500:
                            self.tempanswer = 1
                        elif posx > 590 and posx < 790 and posy > 300 and posy < 500:
                            self.tempanswer = 2
                
    def __updateRoles__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        self.screen.blit(self.questionlist[self.rand], (350, 70))
        for i in range(len(self.answerlist)):
            self.screen.blit(self.answerlist[i], (150 + i * 220, 300)) # (150, 300) (370, 300) (590, 300) 宽高均为200
        
def main():
    finger = Finger()
    finger.startGame()
    
if __name__ == "__main__":
    main()
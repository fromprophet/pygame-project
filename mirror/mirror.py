import pygame
import sys
import time
import random
from gameObject import *
from gamePart import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Mirror(object):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1200, 800))
        self.time = pygame.time.Clock()
        self.chessboard_index = 5 # 控制产生几*几的棋盘
        
    def startGame(self):
        while True:
            self.time.tick(60)
            self.__eventhandler__()
            self.__update__()
            pygame.display.flip()
            
    def __eventhandler__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def __update__(self):
        self.screen.fill("#808080")
        self.screen.blit(pygame.image.load("images/description.png").convert(), (900, 0))
        
def main():
    mirror = Mirror()
    mirror.startGame()
    
if __name__ == "__main__":
    main()
import pygame
from const import *
class Info_board: 
    def __init__(self): 
        self.pink_wins = 0
        self.white_wins = 0
        self.draws = 0

        self.captured_white = 0
        self.captured_pink = 0



    def capture(self, color, captured = False): 
        if (captured): 
            if (color =="white" ):
                self.captured_white = self.captured_white+1 
            else : 
                self.captured_pink = self.captured_pink+1  
    
    
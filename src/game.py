import pygame 
from const import *
from board import *
from dragger import *
from sound import *

class Game : 

    def __init__(self): 
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hover_sqr = None

    def show_bg(self, surface): 
        for row in range (ROW): 
            for col in range(COL): 
                if (row +col)%2==0: 
                    color = (243, 179, 177)
                else : 
                    color = (255, 255, 255)

                rect = (col*SQSIZE, row*SQSIZE,SQSIZE, SQSIZE )
                pygame.draw.rect(surface,color, rect)

    def show_pieces(self, surface): 
        for row in range (ROW): 
            for col in range(COL):
                if self.board.squares[row][col].has_piece(): 
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece :
                        piece.set_texture()
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE //2, row * SQSIZE + SQSIZE //2 #to cennter the image 
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface): 
        if self.dragger.dragging : 
            piece = self.dragger.piece
        
            for move in piece.moves: 
                color = "#C86464" if (move.final.row +move.final.col)%2 ==0 else "#C84546" #different colors for pink and white squares 
                rect = (move.final.col*SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        if self.board.last_move: 
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]: 
                color = (244, 247, 166) if (pos.row +pos.col)%2 ==0 else (172, 195, 51) #different colors for pink and white squares 
                rect = (pos.col*SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self,surface): 
        if self.hover_sqr:
            color = (180, 180, 180) 
            rect = (self.hover_sqr.col*SQSIZE, self.hover_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width =3)

    def set_hover(self, row, col): 
        self.hover_sqr = self.board.squares[row][col]

    def next_turn(self): 
        self.next_player = "white" if self.next_player == "pink" else "pink"

    def sound_effect(self, captured=False): 
        if captured : 
            sound_catch = Sound(os.path.join("assets/sounds/catch.wav"))
            sound_catch.play()
        else : 
            sound_move = Sound(os.path.join("assets/sounds/move.wav"))
            sound_move.play()

    def reset(self): 
        self.__init__()
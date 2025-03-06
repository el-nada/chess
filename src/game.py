import pygame 
from pygame._freetype import init, Font
from const import *
from board import *
from dragger import *
from sound import *
from info_board import *

class Game : 

    def __init__(self): 
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hover_sqr = None
        self.info= Info_board()
        pygame.font.init() 
        self.my_font = pygame.font.SysFont('Comic Sans MS', 40)

    def show_bg(self, surface): 
        for row in range (ROW): 
            for col in range(COL): 
                if (row +col)%2==0: 
                    color = pink_tile
                else : 
                    color = white_tile

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
                color = moves_dark if (move.final.row +move.final.col)%2 ==0 else moves_light #different colors for pink and white squares 
                rect = (move.final.col*SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        if self.board.last_move: 
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]: 
                color = last_move_dark if (pos.row +pos.col)%2 ==0 else last_move_light #different colors for pink and white squares 
                rect = (pos.col*SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self,surface): 
        if self.hover_sqr:
            color = (180, 180, 180) 
            rect = (self.hover_sqr.col*SQSIZE, self.hover_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width =3)

    def set_hover(self, row, col):
        if (row<8 and col<8): 
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

    def show_info(self, surface): 
        
        color = background
        rect = (800, 0,400, HEIGHT )
        pygame.draw.rect(surface, color, rect)
        text_surface = self.my_font.render('Game info', False, (250,250,250))
        surface.blit(text_surface, ((WIDTH-(I_WIDTH+text_surface.get_width())/2),20))

        self.show_turn(surface)
        self.show_timer(surface)
        self.show_captured(surface)

    def show_turn(self, surface): 
        text_surface = self.my_font.render(f"Turn : {self.next_player}", False, (250,250,250))
        surface.blit(text_surface, ((WIDTH-(I_WIDTH+text_surface.get_width())/2),100))

    def show_timer(self, surface): 
        pass 

    def show_captured(self, surface): 
        text_surface = self.my_font.render(f"Captured : {self.info.captured_pink}", False, (250,250,250)) if self.next_player == "pink" else self.my_font.render(f"Captured : {self.info.captured_white}", False, (250,250,250))
        surface.blit(text_surface, ((WIDTH-(I_WIDTH+text_surface.get_width())/2),200))

    def reset(self): 
        self.__init__()
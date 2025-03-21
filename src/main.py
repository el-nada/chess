import pygame 
import sys
from const import *
from game import Game 
from dragger import *
from square import *
from move import *
from info_board import *
from AIplayer import *
class Main : 

    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game=Game()
        self.ai = None
        self.info_board = Info_board()

    def mainloop(self): 
        screen = self.screen
        game = self.game 
        dragger = self.game.dragger
        board = self.game.board
        ai = self.ai
        #info_board = self.info_board

        while True : 
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)
            #game.show_info(screen, self.info_board )

            if game.board.in_check_mate("white") or game.board.in_check_mate("pink"): 
                print("hello")

            if dragger.dragging : 
                dragger.update_blit(screen)

            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    dragger.update_mouse(event.pos) 

                    clicked_row = dragger.mouseY //SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if clicked_col<8 and clicked_row<8 and board.squares[clicked_row][clicked_col].has_piece(): 
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player : 
                            game.board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_hover(screen)
                            game.show_pieces(screen)
                            #game.show_captured(screen, self.info_board)


                elif event.type == pygame.MOUSEMOTION: 
                    motion_row = event.pos[1]//SQSIZE
                    motion_col = event.pos[0]//SQSIZE
                    
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging: 
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        #game.show_info(screen, self.info_board )
                        dragger.update_blit(screen) 
                        

                elif  event.type == pygame.MOUSEBUTTONUP: 
                    if dragger.dragging : 
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        if board.valid_move(dragger.piece, move): 
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                           #info_board.capture(piece.color,captured)

                            game.sound_effect(captured)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_hover(screen)
                            game.show_pieces(screen)
                            #game.show_info(screen, self.info_board )
                            game.next_turn()
                            if (not ai): 
                                ai.choose_move(board)

                    dragger.undrag_piece()

                elif event.type== pygame.KEYDOWN : 
                    if event.key == pygame.K_r : 
                        game.reset()
                        game = self.game 
                        dragger = self.game.dragger
                        board = self.game.board

                    elif event.key == pygame.K_m : # Press the m key to play the min max ai-player
                        print("holallala")
                        game.reset()
                        game = self.game 
                        dragger = self.game.dragger
                        board = self.game.board
                        ai = MinimaxAI("pink")

                elif  event.type == pygame.QUIT : 
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


main = Main()
main.mainloop()
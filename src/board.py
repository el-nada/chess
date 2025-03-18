import copy
from const import *
from square import *
from piece import *
from move import *

class Board : 

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COL)]
        self.last_move = None
        self.create()
        self.add_pieces("white")
        self.add_pieces("pink")

    def create(self): 
        for row in range(ROW): 
            for col in range(COL):
                self.squares[row][col]= Square(row, col)

    def add_pieces(self, color): 
        row_pawn, row_other = (6,7) if color =="white" else (1, 0) 

        for col in range(COL): 
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        #self.squares[5][5] = Square(5, 5, King("pink"))

    def move(self, piece, move): 
        initial = move.initial 
        final = move.final 

        self.squares[initial.row][initial.col].piece= None
        self.squares[final.row][final.col].piece = piece

        # Pawn promotion 
        if isinstance(piece, Pawn): 
            self.check_promotion(piece, final)

        # Caslting 
        if isinstance(piece, King): 
            if self.castling(initial, final): 
                dif = final.col - initial.col
                rook = piece.left_rook if (dif<0) else piece.right_rook
                
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.moves = []
        self.last_move = move

    def valid_move(self, piece, move): 
        return move in piece.moves

    def calc_moves(self, piece, row, col, check=True): # check tells me if I'm looking for check 

        def straightline_moves(incrs):
            for incr in incrs : 
                row_incr, col_incr = incr
                possible_move_r = row + row_incr
                possible_move_c = col + col_incr

                while(True): 
                    if Square.in_range(possible_move_r, possible_move_c): 
                        if self.squares[possible_move_r][possible_move_c].is_empty_or_rival(piece.color): 
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_r][possible_move_c].piece
                            final =Square( possible_move_r, possible_move_c, final_piece)

                            move = Move(initial, final, piece)
                            # check for potential check
                            if check : 
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)

                            else : 
                                piece.add_moves(move)

                            if self.squares[possible_move_r][possible_move_c].is_empty():
                                possible_move_r = possible_move_r + row_incr
                                possible_move_c = possible_move_c + col_incr
                            else : 
                                break
                        else : 
                            break
                    else : 
                        break

        if isinstance(piece, Pawn): 
            steps = 1 if piece.moved else 2
            
            # vertical moves 
            start =  row + piece.dir
            end = row + (piece.dir * (1+ steps))
            for move_row in range(start, end, piece.dir): 
                if Square.in_range(move_row): 
                    if self.squares[move_row][col].is_empty(): 
                        initial = Square(row, col)
                        final =Square( move_row, col)

                        move = Move(initial, final, piece)

                        # check for potential check
                        if check : 
                            if not self.in_check(piece, move):
                                piece.add_moves(move)

                        else : 
                            piece.add_moves(move)

                    else : 
                        break # the pawn is blocked 
                else : 
                    break 

            # diagonal moves 
            possible_moves= [(row+piece.dir, col+1),(row+piece.dir, col-1) ]
            for possible_move in possible_moves: 
                possible_move_r, possible_move_c = possible_move

                if Square.in_range(possible_move_r, possible_move_c): 
                    if self.squares[possible_move_r][possible_move_c].has_rival_piece(piece.color): 
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_r][possible_move_c].piece
                        final =Square( possible_move_r, possible_move_c, final_piece)

                        move = Move(initial, final, piece)
                        # check for potential check
                        if check : 
                            if not self.in_check(piece, move):
                                piece.add_moves(move)

                        else : 
                            piece.add_moves(move)

        if isinstance(piece, Knight): 
            possible_moves = [(row-2, col+1),(row-2, col-1),
                              (row+2, col+1),(row+2, col-1),
                              (row+1, col+2),(row-1, col+2),
                              (row+1, col-2),(row-1, col-2)]
            
            for possible_move in possible_moves: 
                possible_move_r, possible_move_c = possible_move

                if Square.in_range(possible_move_r, possible_move_c): 
                    if self.squares[possible_move_r][possible_move_c].is_empty_or_rival(piece.color): 
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_r][possible_move_c].piece
                        final =Square( possible_move_r, possible_move_c, final_piece)

                        move = Move(initial, final, piece)

                        # check for potential check
                        if check : 
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else : 
                            piece.add_moves(move)

        if isinstance(piece, Bishop): 
            straightline_moves( [(-1,1), (-1, -1), (1, 1), (1, -1)])

        if isinstance(piece, Rook): 
            straightline_moves( [(-1,0), (0, -1), (1, 0), (0, 1)])

        if isinstance(piece, Queen): 
            straightline_moves( [(-1,1), (-1, -1), (1, 1), (1, -1), (-1,0), (0, -1), (1, 0), (0, 1)])

        if isinstance(piece, King): 
            possible_moves = [(row+1, col),(row-1, col),
                              (row, col+1),(row, col-1), 
                              (row+1, col+1),(row+1, col-1),
                              (row-1, col+1),(row-1, col-1)]
            
            for possible_move in possible_moves: 
                possible_move_r, possible_move_c = possible_move

                if Square.in_range(possible_move_r, possible_move_c): 
                    if self.squares[possible_move_r][possible_move_c].is_empty_or_rival(piece.color): 
                        initial = Square(row, col)
                        final =Square( possible_move_r, possible_move_c)

                        move = Move(initial, final, piece)
                        # check for potential check
                        if check : 
                            if not self.in_check(piece, move):
                                piece.add_moves(move)

                        else : 
                            piece.add_moves(move)

            # castling 

            if not piece.moved : 
                if isinstance(self.squares[row][0].piece, Rook) and not self.squares[row][0].piece.moved :
                    left_rook = self.squares[row][0].piece
                    for move_col in range(1, 4): 

                        if self.squares[row][move_col].is_empty(): 

                                if move_col==3: 
                                    piece.left_rook = left_rook

                                    initial = Square(row, 0)
                                    final =Square(row, 3)

                                    move_rook = Move(initial, final , piece.left_rook)

                                    initial = Square(row, col)
                                    final =Square(row, 2)

                                    move_king = Move(initial, final, piece)

                                    # check for potential check
                                    left_rook.add_moves(move_rook)

                                    if check : 
                                        if not self.in_check(piece, move_king) and not self.in_check(left_rook, move_rook) :
                                            left_rook.add_moves(move_rook)
                                            piece.add_moves(move_king)

                                    else : 
                                        left_rook.add_moves(move_rook)
                                        piece.add_moves(move_king)

                                    left_rook.moves.remove(move_rook)

                        else : 
                            break

                if isinstance(self.squares[row][7].piece, Rook) and not self.squares[row][7].piece.moved :
                    right_rook = self.squares[row][7].piece
                    for move_col in range(5, 7): 

                        if self.squares[row][move_col].is_empty(): 

                                if move_col==6: 
                                    piece.right_rook = right_rook

                                    initial = Square(row, 7)
                                    final =Square(row, 5)

                                    move_rook = Move(initial, final, piece.right_rook)

                                    initial = Square(row, col)
                                    final =Square(row, 6)

                                    move_king = Move(initial, final, piece)

                                    # check for potential check
                                    right_rook.add_moves(move_rook)

                                    if check : 
                                        if not self.in_check(piece, move_king) and not self.in_check(right_rook, move_rook) :
                                            
                                            right_rook.add_moves(move_rook)
                                            piece.add_moves(move_king)

                                    else : 
                                        right_rook.add_moves(move_rook)
                                        piece.add_moves(move_king)

                                    right_rook.moves.remove(move_rook)
                        else : 
                            break

    def check_promotion(self, piece, final) : 
        if final.row == 0 or final.row ==7 : 
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final): 
        return abs(initial.col -final.col)==2 
    
    def in_check(self, piece, move):
        # Simulate the move on a temporary board
        temp_board = copy.deepcopy(self)
        temp_piece = copy.deepcopy(piece)
        temp_board.move(temp_piece, move)

        return temp_board.is_king_in_check(temp_piece.color)
    
    def is_king_in_check(self, color):
        king_pos = None
        for row in range(ROW):
            for col in range(COL):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
    
        for row in range(ROW):
            for col in range(COL):
                piece = self.squares[row][col].piece
                if piece and piece.color != color:
                    self.calc_moves(piece, row, col, check=False)
                    for move in piece.moves:
                        if (move.final.row, move.final.col) == king_pos:
                            return True
        return False
    
    def in_check_mate(self, color):
        temp_board = copy.deepcopy(self)
        if not temp_board.is_king_in_check(color):
            return False

        for row in range(ROW):
            for col in range(COL):
                if temp_board.squares[row][col].has_team_piece(color):
                    piece = temp_board.squares[row][col].piece
                    temp_board.calc_moves(piece, row, col, check=True)
                    if piece.moves:  
                        return False
        return True  



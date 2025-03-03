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

    def calc_moves(self, piece, row, col): 

        def straightline_moves(incrs):
            for incr in incrs : 
                row_incr, col_incr = incr
                possible_move_r = row + row_incr
                possible_move_c = col + col_incr

                while(True): 
                    if Square.in_range(possible_move_r, possible_move_c): 
                        if self.squares[possible_move_r][possible_move_c].is_empty_or_rival(piece.color): 
                            initial = Square(row, col)
                            final =Square( possible_move_r, possible_move_c)

                            move = Move(initial, final)
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

                        move = Move(initial, final)
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
                        final =Square( possible_move_r, possible_move_c)

                        move = Move(initial, final)
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
                        final =Square( possible_move_r, possible_move_c)

                        move = Move(initial, final)
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

                        move = Move(initial, final)
                        piece.add_moves(move)

            # castling 

            if not piece.moved : 
                if isinstance(self.squares[row][0].piece, Rook) and not self.squares[row][0].piece.moved :
                    for move_col in range(1, 4): 

                        if self.squares[row][move_col].is_empty(): 

                                if move_col==3: 
                                    piece.left_rook = self.squares[row][0].piece

                                    initial = Square(row, 0)
                                    final =Square(row, 3)

                                    move = Move(initial, final)
                                    self.squares[row][0].piece.add_moves(move)

                                    initial = Square(row, col)
                                    final =Square(row, 2)

                                    move = Move(initial, final)
                                    piece.add_moves(move)

                        else : 
                            break

                if isinstance(self.squares[row][7].piece, Rook) and not self.squares[row][0].piece.moved :
                    for move_col in range(5, 7): 

                        if self.squares[row][move_col].is_empty(): 

                                if move_col==6: 
                                    piece.right_rook = self.squares[row][7].piece

                                    initial = Square(row, 7)
                                    final =Square(row, 5)

                                    move = Move(initial, final)
                                    self.squares[row][7].piece.add_moves(move)

                                    initial = Square(row, col)
                                    final =Square(row, 6)

                                    move = Move(initial, final)
                                    piece.add_moves(move)

                        else : 
                            break

                                       
    
    def check_promotion(self, piece, final) : 
        if final.row == 0 or final.row ==7 : 
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final): 
        return abs(initial.col -final.col)==2 
    


class Square : 

    def __init__(self, row, col, piece=None):
        self.row= row
        self.col=col
        self.piece= piece

    def has_piece(self): 
        return self.piece != None

    def has_team_piece(self, color): 
        return self.has_piece() and self.piece.color==color
    
    def has_rival_piece(self, color): 
        return self.has_piece() and self.piece.color!=color
    
    def is_empty_or_rival(self, color): 
        return self.has_rival_piece(color) or not self.has_piece()
    
    def is_empty(self): 
        return not self.has_piece()
    
    @staticmethod
    def in_range(*args):
        for arg in args : 
            if arg<0 or arg >7 : 
                return False 
        return True
    
    def __eq__(self, other): 
        return self.row == other.row and self.col == other.col
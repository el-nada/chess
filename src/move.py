class Move : 
    def __init__(self, initial, final, piece = None):
        self.initial = initial
        self.final = final
        self.piece = piece

    

    def __eq__(self, other): 
        return self.initial == other.initial and self.final == other.final
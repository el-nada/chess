from const import *
import copy
from abc import ABC, abstractmethod
import time

class AIPlayer(ABC):
    def __init__(self, color, max_depth=3, time_limit=5):
        self.color = color  # 'white' or 'pink'
        self.max_depth = max_depth  # Max search depth
        self.time_limit = time_limit  # Time limit for iterative deepening

    @abstractmethod
    def choose_move(self, board):
        """All AI subclasses must implement this method."""
        pass

    def get_legal_moves(self, board, color):
        legal_moves = []
        for row in range(ROW):
            for col in range(COL):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    piece = square.piece
                    board.calc_moves(piece, row, col, check=True)
                    legal_moves.extend(piece.moves) # appends all moves of the current piece to the legal_moves
        return legal_moves

    def evaluate_board(self, board):
        """Basic evaluation function (material advantage + positional heuristics)."""
        material = 0
        for row in range(ROW):
            for col in range(COL):
                piece = board.squares[row][col].piece
                if piece:
                    value = piece.value
                    material += value if piece.color == self.color else - value
        return material
    

class MinimaxAI(AIPlayer):

    def choose_move(self, board):
        best_move = None
        best_value = -float('inf')
        legal_moves = self.get_legal_moves(board, self.color)
        
        for move in legal_moves:
            board_copy = copy.deepcopy(board)
            board_copy.move(move.piece, move)
            value = self.minimax(board_copy, self.max_depth, -float('inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.in_check_mate(self.color):
            return self.evaluate_board(board)
        
        if maximizing:
            max_eval = -float('inf')
            for move in self.get_legal_moves(board, self.color):
                board_copy = copy.deepcopy(board)
                board_copy.move(move.piece, move)
                eval = self.minimax(board_copy, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_color = 'pink' if self.color == 'white' else 'white'
            for move in self.get_legal_moves(board, opponent_color):
                board_copy = copy.deepcopy(board)
                board_copy.move(move.piece, move)
                eval = self.minimax(board_copy, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
# Chess Game

A classic chess game implemented in Python with a graphical user interface, supporting standard chess rules including check, checkmate, castling, en passant, and pawn promotion.

## Features

- **Full Chess Rules**:  
    Valid moves for all pieces (pawn, rook, knight, bishop, queen, king)  
    Check/checkmate detection  
    Castling (kingside and queenside)  
    En passant capture  
    Pawn promotion to queen  

- **Game Interface**:  
  Turn indicator (white/pink)  
   Move history panel  
   Captured pieces tracker  
   Game status alerts (check, checkmate, stalemate)   

---

##  Technologies Used

- Python 3.8+
- Pygame library (for GUI)

## How to play 

- Move Pieces: Click and drag a piece to a valid square.
- Castling: Move the king two squares toward the rook.
- Pawn Promotion: Automatically promoted to queen upon reaching the back rank.
- R: Reset the game

## Project structure 

```
chess/

├── src/
│   ├── main.py        # Entry point and GUI setup
│   ├── board.py       # Board logic and piece movement
│   ├── piece.py       # Piece classes (Pawn, Rook, etc.)
│   ├── ...            # other game logic files
│   └── constants.py   # Colors, dimensions
├── assets/            # Folder for static assets
│   ├── images         # Piece images 
│   └── sounds         # Sound effect for moves 
└── README.md
```
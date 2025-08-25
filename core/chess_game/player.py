from __future__ import annotations
import importlib
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece import ChessPieces, king
    from .Board import ChessBoard

from typing import List, Optional

class Player():
    def __init__(self, user_id: str, name: str, color: str):
        self.user_id = user_id     # ID duy nhất từ DB, JWT, v.v.
        self.name = name
        self.color = color
        self.pieces = []
        self.king_position = None
        self.opponent = None
        self.board = None

    def get_color(self):
        return self.color

    def set_color(self,color:str):
        self.color = color

    def set_board(self, board:'ChessBoard'):
        self.board = board

    def get_board(self) -> Optional['ChessBoard']:
        return self.board

    def set_opponent(self, opponent: 'Player'):
        self.opponent = opponent

    def get_opponent(self) -> Optional['Player']:
        return self.opponent

    def get_id(self):
        return self.user_id
    
    def get_king(self):
        king_module = importlib.import_module("core.piece.king")
        king = king_module.King
        for piece in self.pieces:
            if isinstance(piece, king) and not piece.is_captured():
                return piece
        return None
    
    def get_score(self) -> int:
        return sum(piece.value for piece in self.pieces if not piece.is_captured())
    
    def remove_piece(self, piece):
        if piece in self.pieces:
            r, c = piece.get_position()
            index = r * 8 + c
            # self.pieces.remove(piece) # xoa object piece khoi list pieces
            self.get_board().remove_piece(index) # xoa object piece khoi ban co
            piece.remove() # set captured = true, position = none



    
    def set_piece(self, piece: ChessPieces):
        self.pieces.append(piece)
        piece.set_player(self)

    def get_pieces(self) -> List[ChessPieces]:
        return self.pieces
    
    def __str__(self):
        return f"Player({self.name}, {self.color}, {self.get_score()})"

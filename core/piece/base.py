from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.chess_game.player import Player

class ChessPieces(ABC):

    def __init__(self,  value, color, player:'Player', position=None, captured = False):
        self.value = value
        self.color = color
        self.position = position # position = [r,c]
        self.captured = captured
        self.player = player
        self.symbol = None

    @abstractmethod
    def get_attack_square(self):
        pass
    @abstractmethod
    def get_type(self):
        pass
    def legal_move(self):
        board = self.get_player().get_board()
        legal_moves = []
        moves = self.get_attack_square()
        for move in moves:
            if not board.would_expose_king(self.position[0] * 8 + self.position[1],move ): # tao 1 method would_expose_king() trong board
                row, col = divmod(move, 8)
                legal_moves.append([row, col])

        return legal_moves

    def get_position(self):
        return self.position

    def get_index(self):
        return self.position[0] * 8 + self.position[1]

    def set_position(self, new_position):
        self.position = new_position

    def is_captured(self):
        return self.captured

    def set_captured(self, state:bool):
        self.captured = state
        
    def get_value(self):
        return self.value

    def get_color(self):
        return self.color
    
    
    def set_color(self,color: str):
        self.color = color

    def get_player(self):
        return self.player
    def set_player(self, player: 'Player'):
        self.player = player

    def remove(self):
        """Khi quân bị ăn, gán trạng thái captured = True và xóa vị trí"""
        self.captured = True
        self.position = None

    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, pos={self.position})"

    __repr__ = __str__  # dùng lại luôn



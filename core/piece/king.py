from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode
else:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode
   

class King(ChessPieces):
    def __init__(self, color,player, position):
        if position is None:
            position = [0, 4] if color == "white" else [7, 4]
        super().__init__(value=100, color=color,player = player, position=position)
        self.symbol = ChessPiecesUnicode.PIECE_UNICODE[color]["king"]
        self.hasmove = False

        


    def get_attack_square(self):
        moves = []
        for i in range(self.position[0] - 1, self.position[0] + 2):
            for j in range(self.position[1] - 1, self.position[1] + 2):
                # Bỏ qua chính ô của quân vua
                if i == self.position[0] and j == self.position[1]:
                    continue
                # Chỉ xét các ô nằm trong bàn cờ
                if 0 <= i < 8 and 0 <= j < 8:
                    idx = i * 8 + j
                    piece = self.get_player().get_board().get_piece(idx)
                    if piece is None or piece.get_color() != self.color:
                        moves.append(idx)
        return moves


    def legal_move(self):
        return super().legal_move()


    def get_position(self):
        return super().get_position()

    def set_position(self, new_position):
        return super().set_position(new_position)

    def is_captured(self):
        return super().is_captured()

    def set_captured(self, state):
        return super().set_captured(state)
    
    def get_color(self):
        return super().get_color()
    
    def set_color(self, color):
        return super().set_color(color)

    def set_player(self, player):
        return super().set_player(player)
    
    def get_player(self):
        return super().get_player()

    def remove(self):
        return super().remove()
    

    def get_value(self):
        return super().get_value()
    def set_hasmove(self):
        self.hasmove = True
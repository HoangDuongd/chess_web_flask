from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode
else:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode

class Knight(ChessPieces):


    def __init__(self,color,player, position):
        super().__init__(value=3, color=color,player=player, position=position)
        self.symbol = ChessPiecesUnicode.PIECE_UNICODE[color]["knight"]

    def get_attack_square(self):
        board = self.get_player().get_board()
        moves = []
        r, c = self.position
        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                idx = nr * 8 + nc
                piece = board.get_piece(idx)
                if piece is None or piece.get_color() != self.color:
                    moves.append(idx)

        return moves
    



    def legal_move(self):
        return super().legal_move()


    def set_position(self, new_position):
        return super().set_position(new_position)

    def get_position(self):
        return super().get_position()

    def is_captured(self):
        return super().is_captured()

    def set_captured(self, state):
        return super().set_captured(state)

    def get_color(self):
        return super().get_color()
    

    def set_color(self, color):
        return super().set_color(color)

    def get_player(self):
        return super().get_player()

    def set_player(self, player):
        return super().set_player(player)
    
    def remove(self):
        return super().remove()
    def get_value(self):
        return super().get_value()
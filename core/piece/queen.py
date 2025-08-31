from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode
else:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode


class Queen(ChessPieces):
    def __init__(self, color,player, position):
        if position is None:
            position = [0,3] if color == "white" else [7,3]
        super().__init__(value=9, color=color,player=player, position=position)
        self.symbol = ChessPiecesUnicode.PIECE_UNICODE[color]["queen"]
    



    def get_attack_square(self):
        board = self.get_player().get_board()
        moves = []
        if self.get_position() is not None:
            r, c = self.position

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1,1), (-1,-1), (1,-1), (-1,1)]  # Lên, xuống, trái, phải


            for dr, dc in directions:
                i, j = r + dr, c + dc
                while 0 <= i < 8 and 0 <= j < 8:
                    idx = i * 8 + j
                    target = board.get_piece(idx)
                    if target is None:
                        moves.append(idx)
                    elif target.get_color() == self.get_color():
                        break
                    else:  # khác màu
                        moves.append(idx)
                        break
                    i += dr
                    j += dc

        return moves



    def legal_move(self):
        return super().legal_move()
    
    def get_position(self):
        return super().get_position()

    def get_index(self):
        return super().get_index()

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
    
    def get_player(self):
        return super().get_player()

    def set_player(self, player):
        return super().set_player(player)
    
    def remove(self):
        return super().remove()
        
    def get_value(self):
        return super().get_value()
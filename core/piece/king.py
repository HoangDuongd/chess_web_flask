from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece.base import ChessPieces
    from core.piece.rook import Rook
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
        self.Rook_Queen = None
        self.Rook_King = None

        


    def get_attack_square(self):
        board = self.get_player().get_board()
        moves = []
        # normal move
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
        # castle move
        castle_moves = [self.get_castle_move(self.get_Rook_Kingside()),self.get_castle_move(self.get_Rook_Queenside())]
        for castle_move in castle_moves:
            if castle_move is not None:
                moves.append(castle_move)

        return moves


    def get_castle_move(self, piece:'Rook'):
        board = self.get_player().get_board()
        step = 1 if self.get_Rook_Kingside() == piece else -1
        if not self.get_hasmove() and not piece.get_hasmove():
            if self.get_Rook_Kingside() == piece or self.get_Rook_Queenside() == piece:
                for index in range(self.get_index() + step, piece.get_index(), step):
                    if board.get_piece(index) is not None:
                        return None
                return self.get_index() + step * 2
        return None
            


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

    def get_hasmove(self):
        return self.hasmove
    
    def set_Rook(self, piece:'Rook',side):
        if side == "Queen":
            self.Rook_Queen = piece
        else:
            self.Rook_King = piece
    def get_Rook_Queenside(self):
        return self.Rook_Queen
    def get_Rook_Kingside(self):
        return self.Rook_King
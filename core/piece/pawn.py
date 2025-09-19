from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode
else:
    from core.piece.base import ChessPieces
    from core.piece.constant import ChessPiecesUnicode



class Pawn(ChessPieces):


    def __init__(self,color,player, position):
        ChessPieces.__init__(self, value=1, color=color,player=player, position = position)
        self.symbol = ChessPiecesUnicode.PIECE_UNICODE[color]["pawn"]

    def get_attack_square(self):
        board = self.get_player().get_board()
        moves = []
        r, c = self.position

        direction = 1 if self.get_color() == "white" else -1
        start_row = 1 if self.get_color() == "white" else 6

        # --- Đi thẳng ---
        one_step = (r + direction) * 8 + c
        if 0 <= r + direction < 8 and board.get_piece(one_step) is None:
            moves.append(one_step)

            # Đi 2 bước từ vị trí xuất phát
            if r == start_row:
                two_step = (r + 2 * direction) * 8 + c
                if board.get_piece(two_step) is None:
                    moves.append(two_step)

        # --- Ăn chéo ---
        for dc in (-1, 1):
            nc = c + dc
            nr = r + direction
            if 0 <= nc < 8 and 0 <= nr < 8:
                diag = nr * 8 + nc
                piece = board.get_piece(diag)
                if piece and piece.get_color() != self.get_color():
                    moves.append(diag)

        # --- Bắt tốt qua đường (en passant) ---
        last_move = board.get_game().last_move()
        if last_move:
            from_idx, to_idx, moved_piece,category, promotion = last_move
            if moved_piece.__class__.__name__ == "Pawn":
                fr, fc = divmod(from_idx, 8)
                tr, tc = divmod(to_idx, 8)

                # Kiểm tra nếu đối thủ vừa đi tốt 2 ô
                if abs(fr - tr) == 2 and tr == r:  
                    # Nếu tốt của ta đang cạnh ngang (trái hoặc phải)
                    if abs(tc - c) == 1:
                        # Ô sau lưng tốt đối thủ (nơi ta sẽ ăn qua đường)
                        en_passant_square = (r + direction) * 8 + tc
                        moves.append(en_passant_square)

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
    
    def get_player(self):
        return super().get_player()

    def set_player(self, player):
        return super().set_player(player)
    

    def remove(self):
        return super().remove()
    
    def get_value(self):
        return super().get_value()
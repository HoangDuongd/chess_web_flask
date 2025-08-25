from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.piece import King,Queen,Bishop,Knight,Rook,Pawn
    from .player import Player
    from .Game import ChessGame
else:
    from core.piece import King,Queen,Bishop,Knight,Rook,Pawn






class ChessBoard():
    def __init__(self):
        self.grid = [None] * 64
        self.players = [None] * 2
        self.game = None
        self.move = []


    

    def set_players(self, player1:'Player', player2:'Player'):
        self.players[0] = player1
        self.players[1] = player2

    def setup_default_position(self):
        player1 = self.players[0]
        player2 = self.players[1]
        # Bản đồ cấu trúc ban đầu: (index -> (PieceClass, color))
        piece_map = {
            0: (Rook, "white",player1), 1: (Knight, "white",player1), 2: (Bishop, "white",player1),
            3: (Queen, "white",player1), 4: (King, "white",player1), 5: (Bishop, "white",player1),
            6: (Knight, "white",player1), 7: (Rook, "white",player1),
            56: (Rook, "black",self.players[1]), 57: (Knight, "black",player2), 58: (Bishop, "black",player2),
            59: (Queen, "black",player2), 60: (King, "black",player2), 61: (Bishop, "black",player2),
            62: (Knight, "black",player2), 63: (Rook, "black",player2),
        }

        # Khởi tạo các quân cờ chính
        for index, (PieceClass, color,player) in piece_map.items():
            row, col = divmod(index, 8)
            self.grid[index] = PieceClass(color=color,player=player, position=[row, col])

        # Khởi tạo tốt (pawn)
        for i in range(8):
            self.grid[8 + i] = Pawn(color="white",player=player1, position=[1, i])
            self.grid[48 + i] = Pawn(color="black",player=player2, position=[6, i])



    def get_piece(self, index):
        return self.grid[index]


    def move_piece(self, from_index, to_index):
        piece = self.get_piece(from_index)
        position = list(divmod(to_index, 8))
        if piece is not None :
            if piece.get_color() == self.get_game().get_current_turn():
                if  position in piece.legal_move():
                    target = self.get_piece(to_index)
                    if target is not None:
                        target.get_player().remove_piece(target)
                        # (Optionally: gọi player.remove_piece(target) nếu bạn quản lý player)

                    self.grid[to_index] = piece
                    self.grid[from_index] = None
                    row, col = divmod(to_index, 8)
                    piece.set_position(new_position = [row, col])
                    if isinstance(piece, King) or isinstance(piece, Rook):
                        piece.set_hasmove()
                     # --- Kiểm tra promotion ---
                    from core.piece.pawn import Pawn  # tránh circular import thì đặt TYPE_CHECKING như bạn làm
                    if isinstance(piece, Pawn):
                        last_row = 7 if piece.get_color() == "white" else 0
                        if row == last_row:
                            self.promote_to_queen(to_index)

                    # Ghi lại nước đi
                    self.add_move((from_index, to_index, piece))

                    # Chuyển lượt
                    self.get_game().switch_turn()


        if self.checkmate(to_index):
            self.get_game().end_game(piece.get_player())

        

    def remove_piece(self, index):
        self.grid[index] = None
    
    def simulate_move(self, from_index, to_index):
        piece = self.get_piece(from_index)
        captured = self.get_piece(to_index)
        if captured is not None:
            captured.set_captured(True)
        self.grid[to_index] = piece
        self.grid[from_index] = None
        piece.set_position([to_index // 8, to_index % 8])
        return captured

    def undo_simulated_move(self, from_index, to_index, captured_piece):
        piece = self.get_piece(to_index)
        self.grid[from_index] = piece
        if captured_piece is not None:
            captured_piece.set_captured(False)
        self.grid[to_index] = captured_piece
        piece.set_position([from_index // 8, from_index % 8])



    def would_expose_king(self,from_index,to_index):
        expose_king = False
        piece = self.get_piece(from_index)
        if piece is not None:
            player = piece.get_player()
            opponent = piece.get_player().get_opponent()
            
            captured = self.simulate_move(from_index, to_index)
            for enemy_piece in opponent.get_pieces():
                if enemy_piece.is_captured() == False:
                    king = player.get_king()
                    if king is not None:
                        king_pos = king.get_position()
                        if king_pos is None:
                            continue
                        king_index = king_pos[0] * 8 + king_pos[1]
                        if king_index in enemy_piece.get_attack_square():
                            expose_king = True
                            break
            self.undo_simulated_move(from_index, to_index, captured)
        return expose_king
            



    def set_game(self, game:'ChessGame'):
        self.game = game

    def get_game(self):
        return self.game

    def castling(self):
    # nhập thành
        pass

    def checkmate(self, index):
        # chiếu hết
        legal_moves = []
        piece = self.get_piece(index)
        if piece is not None:
            opponent = piece.get_player().get_opponent()
            opponent_king_piece = opponent.get_king()
            if opponent_king_piece.is_captured():
                return True
            else:
                r, c = opponent_king_piece.get_position()
                index_king_piece = [r,c]
                if index_king_piece  in piece.legal_move():
                    for opponent_piece in opponent.get_pieces():
                        if not opponent_piece.is_captured():
                            legal_moves.extend(opponent_piece.legal_move())
                    return True if len(legal_moves) == 0 else False
                else:
                    return False
            
        return False



    def promote_to_queen(self, index):
        piece = self.get_piece(index)
        if isinstance(piece, Pawn):
            row, col = piece.get_position()
            if (piece.get_color() == "white" and row == 7) or \
               (piece.get_color() == "black" and row == 0):
                self.grid[index] = Queen(piece.get_color(), piece.get_player(), [row, col])
                piece.get_player().replace_piece(piece, self.grid[index]) # replace_piece(piece, self.grid[index]) chua code ham nay



    def to_unicode_matrix(self):
        board_matrix = [[None for _ in range(8)] for _ in range(8)]
        x = 0
        for square in self.grid:  # Giả sử self.grid là ma trận 8x8 quân cờ hoặc None
            i, j = divmod(x, 8)
            if square:
                 board_matrix[i][j] = square.symbol
            else:
                board_matrix[i][j] = square
            x += 1
        
        return board_matrix
    
    def add_move(self, move):
        self.move.append(move)
    
    def last_move(self):
        return self.move[-1] if self.move else None

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.piece import ChessPieces
    from .Board import ChessBoard
    from core.piece import King,Queen,Bishop,Knight,Rook,Pawn
else:
    from core.piece import King,Queen,Bishop,Knight,Rook,Pawn
from typing import Optional, Type


class Move():
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        self.from_index = from_index
        self.to_index = to_index
        self.piece = piece
        self.captured_piece = None
        self.promotion_piece = None

    def apply(self, board:'ChessBoard'):
        target = board.get_piece(self.to_index)
        if target is not None:
            # capture
            self.captured_piece = target
            board.remove_piece(self.to_index)
        board.set_piece(self.to_index, self.piece)
        
        return "capture" if self.captured_piece is not None else "move"
    def get_from_idx(self):
        return self.from_index
    def get_to_idx(self):
        return self.to_index
    def get_moved_piece(self):
        return self.piece
    def get_captured_piece(self):
        return self.captured_piece
    def get_promotion_piece(self):
        return self.promotion_piece
    
class Capture(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)
    
    def apply(self, board:'ChessBoard'):
        board.remove_piece(self.to_index)
        board.set_piece(self.to_index, self.piece)
        return "capture"

class En_passant(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)
    
    def apply(self, board):
        if self.piece.get_color() == "white":
            self.captured_piece = board.get_piece(self.to_index-8)
        else:
            self.captured_piece = board.get_piece(self.to_index+8)

        board.remove_piece(self.captured_piece.get_index())
        board.set_piece(self.to_index, self.piece)
        return "en passant"
    
class CastleMove(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)
    
    def apply(self, board:'ChessBoard'):
        if isinstance(self.piece, King):
            if abs(self.from_index - self.to_index) == 2:
                if self.to_index > self.from_index: 
                    board.set_piece(self.to_index, self.piece)
                    board.set_piece(self.to_index - 1, self.piece.get_Rook_Kingside()) 
                    return "castle_kingside"
                else:
                    board.set_piece(self.to_index, self.piece)
                    board.set_piece(self.to_index + 1, self.piece.get_Rook_Queenside())
                    return "castle_queenside"
            
            


class Promotion(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces',Prom: Type):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)
        self.Prom = Prom

    def apply(self, board:'ChessBoard'):
        target = board.get_piece(self.to_index)
        if target is not None:
            # capture
            self.captured_piece = target
            board.remove_piece(self.to_index)
        r,c = divmod(self.to_index, 8)
        new_prom = self.Prom(self.piece.get_color(), self.piece.get_player(), position = [r,c])
        board.set_piece(self.to_index, new_prom)
        board.remove_piece(self.from_index)
        return "promotion"


class Check(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)
    
    def apply(self, board:'ChessBoard'):
        board.set_piece(self.to_index, self.piece)
        return "check"

class CheckMate(Move):
    def __init__(self, from_index, to_index, piece:'ChessPieces'):
        Move.__init__(self, from_index=from_index, to_index=to_index, piece=piece)

    def apply(self, board:'ChessBoard'):
        board.set_piece(self.to_index, self.piece)
        board.get_game().end_game(self.piece.get_color())
        return "checkmate"     

class MoveFactory():
    def create(from_index, to_index, piece:'ChessPieces', promotion_choice:Optional[Type] = None):
        board = piece.get_player().get_board()
        opponent = piece.get_player().get_opponent()
        target_piece = board.get_piece(to_index)
        r,_ = divmod(to_index,8)
        if target_piece is not None:
            if target_piece.get_color() != piece.get_color(): # check condition if it is capture move

                if target_piece.get_position() in piece.legal_move():                      # check condition of promotion move
                    if isinstance(piece, Pawn):
                        last_row = 7 if piece.get_color() == "white" else 0
                        if r == last_row:
                            return Promotion(from_index, to_index, piece, promotion_choice)
                        else:
                            return Capture(from_index, to_index, piece)             
                    else:
                        return Capture(from_index, to_index, piece)
        if target_piece is None:
            if isinstance(piece, Pawn):
                last_row = 7 if piece.get_color() == "white" else 0
                if r == last_row:
                    return Promotion(from_index, to_index, piece, promotion_choice)
                elif from_index % 8 != to_index % 8:
                    return En_passant(from_index, to_index, piece)
                else:
                    return Move(from_index, to_index, piece)
                    
            elif isinstance(piece, King) and abs(to_index - from_index) == 2:
                return CastleMove(from_index, to_index, piece)
            else:
                return Move(from_index, to_index, piece)
            
class MoveResult():
    def __init__(self,move:Move, TypeMove:str, is_check:False, is_checkmate:False, is_stalemate:False):
        self.move = move
        self.TypeMove = TypeMove
        self.is_check = is_check
        self.is_checkmate = is_checkmate
        self.is_stalemate = is_stalemate
    def get_move(self):
        return self.move
    def get_typemove(self):
        return self.TypeMove
    
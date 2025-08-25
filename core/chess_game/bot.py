from core.AI.minimax import minimax
from .player import Player
class Bot_ROOKIE(Player):
    def __init__(self, user_id, name, color):
        super().__init__(color, user_id=0, name="ROOKIE")
        self.bot_type = 'ROOKIE'
    def get_board(self):
        return super().get_board()
    def get_color(self):
        return super().get_color()
    def get_king(self):
        return super().get_king()
    def get_opponent(self):
        return super().get_opponent()
    def get_pieces(self):
        return super().get_pieces()
    def get_score(self):
        return super().get_score()
    def set_board(self, board):
        return super().set_board(board)
    def set_color(self, color):
        return super().set_color(color)
    def set_opponent(self, opponent):
        return super().set_opponent(opponent)
    def set_piece(self, piece):
        return super().set_piece(piece)
    
    def __str__(self):
        return super().__str__()
    
    def play_game(self):
        if self.get_board().get_game().get_current_turn() == self.color:
            # from_index, to_index = minimax(self.get_board().get_game(), self, 10, True, 10)
            move = minimax(self.get_board().get_game(), self, 10, True, 10)
            self.get_board().move_piece(move[0], move[1])
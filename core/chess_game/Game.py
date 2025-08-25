from __future__ import annotations
from typing import TYPE_CHECKING
from app.db import SessionLocal
from app.models.Game_history import Game
if TYPE_CHECKING:
    from chess_game import ChessBoard
    from chess_game import Player
else:
    from core.chess_game import ChessBoard

class ChessGame():
    def __init__(self, player1: 'Player', player2: 'Player', typegame:str):
        self.players = [player1, player2]
        self.board: 'ChessBoard' = ChessBoard()
        self.current_turn = "white"  # hoặc random
        self.winner = None
        self.ended = False
        self.setup()
    

    def setup(self):
        self.get_board().set_game(self)
        self.assign_players_to_board()
        self.board.setup_default_position()
        self.assign_pieces_to_players()
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])
        
        
        
    def assign_players_to_board(self):
        self.players[0].set_board(self.board)
        self.players[1].set_board(self.board)
        self.board.set_players(self.players[0], self.players[1])


    def assign_pieces_to_players(self):
        for piece in self.board.grid:
            if piece:
                for player in self.players:
                    if player.color == piece.color:
                        player.set_piece(piece)

    def get_typegame(self):
        return self.get_typegame

    def get_board(self):
        return self.board
    
    def get_current_turn(self):
        return self.current_turn

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def end_game(self, player: 'Player'):
        self.winner = player.get_color()
        self.ended = True

    def get_whitePlayer(self):
        return self.players[0] if self.players[0].get_color() == "white" else  self.players[1]
    def get_blackPlayer(self):
        return self.players[0] if self.players[0].get_color() == "black" else  self.players[1]

    def Game_status(self):
        return self.ended
    
    def get_winner(self):
        return self.winner
    
    def save_db(self):
        db = SessionLocal() #  create database session
        try:
            result = self.get_winner()
            game = Game(
                Type_game = self.get_typegame(), 
                White_player=self.get_whitePlayer().get_id(), 
                Black_player = self.get_blackPlayer().get_id(), 
                Result=result
                )
            db.add(game)
            db.commit()
        finally:
            db.close()
    
# class factory_pattern():
#     def __init__(self, game: ChessGame):
#         self.session = SessionLocal()




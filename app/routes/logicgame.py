from flask import Flask, render_template, jsonify, request, Blueprint, session
from app.db import SessionLocal
import os
import sys
from core.chess_game.player import Player
from core.chess_game.Game import ChessGame
from core.chess_game.bot import Bot_ROOKIE


# --- Khởi tạo Game ---
player1 = Player("1", "Trắng", "white")
# player2 = Player("2", "Đen", "black")                 * sua dong nay, ti sua lai
bot = Bot_ROOKIE("2", "Đen", "black")    
game = ChessGame(player1, bot)

chessgame_bp = Blueprint('logicgame', __name__)





@chessgame_bp.route("/api/board")
def get_board():
    db = SessionLocal()

    # Gửi trạng thái bàn cờ dưới dạng mảng 2D Unicode
    board_state = game.get_board().to_unicode_matrix()
    return jsonify({"board": board_state})


@chessgame_bp.route("/api/piece")
def get_piece(): # add the object game as parameter into this function

    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    index = x * 8 + y
    piece = game.get_board().get_piece(index)
    return jsonify({"exists": piece is not None})

@chessgame_bp.route("/api/legal_moves")
def get_legal_moves(): # add the object game as parameterr into this function
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    index = x * 8 + y
    board = game.get_board()
    piece = board.get_piece(index)
    player_id = session["user_id"]
    if (not piece or piece.color != game.get_current_turn()) and piece.get_player().get_id() == player_id:
        return jsonify({"moves": [], "turn": game.current_turn})

    moves = piece.legal_move()
    return jsonify({"moves": moves, "turn": game.current_turn})

@chessgame_bp.route("/api/move", methods=["POST"])
def make_move(): # add the object game as parameterr into this function
    data = request.get_json()
    from_pos = data["from"][0] * 8 + data["from"][1]
    to_pos = data["to"][0] * 8 + data["to"][1]
    game.get_board().move_piece(from_pos, to_pos)
    if game.Game_status():
        return jsonify({
            "status": "end",
            "winner": game.get_winner()  # "white" hoặc "black"
        })

    return jsonify({
        "status": "ok",
        "next_turn": game.current_turn
    })

# sua lai dong nay

@chessgame_bp.route("/api/bot-move", methods=["POST"])
def bot_move():
    move = bot.play_game()  # Bot chọn nước đi
    return jsonify({
        "bot_move": move,
        "board": game.board.serialize()  # serialize() để trả trạng thái bàn cờ
    })
#
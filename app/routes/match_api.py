from flask import Blueprint, request, jsonify, url_for, session, render_template
from app.db import SessionLocal
from app.models.User import User
from core.chess_game.bot import Bot_ROOKIE
from core.chess_game.player import Player
from core.chess_game.Game import ChessGame


match_bp = Blueprint('match_api',__name__)

@match_bp.route("/api/matchbot")
def match_bot():
    db = SessionLocal()
    try:
        user_id = session["user_id"]
        if user_id is None:
            return render_template("login-page")
        else:
            user = db.get(User, user_id)
            player1 = Player(user.id, user.username, "white")
            bot = Bot_ROOKIE(color="black")
            game = ChessGame(player1, bot)
            return jsonify({
                "status": "ok"
            })
    finally:
        db.close()
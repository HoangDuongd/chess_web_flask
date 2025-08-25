from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.chess_game.player import Player
from core.chess_game.bot import Bot_ROOKIE
from core.chess_game.Game import ChessGame
from app.routes.logicgame import chessgame_bp
from app.routes.User_routes import user_bp
from app.routes.match_api import match_bp
from .config import Config
from app.db import Base, engine
from app.db import SessionLocal
from app.models.User import User
from datetime import timedelta


Base.metadata.create_all(engine)
def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static")),
    )
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)
    # register blueprint:

    app.register_blueprint(chessgame_bp)    
    app.register_blueprint(user_bp)
    app.register_blueprint(match_bp)
    return app
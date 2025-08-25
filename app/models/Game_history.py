from sqlalchemy import create_engine, Text, MetaData, Table, Column, Integer, String, Float, Boolean, ForeignKey, Date,  Enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.db import Base

class Game(Base):
    __tablename__ = "Game_history"
    ID_game = Column(Integer,unique=True, primary_key=True)
    Type_game = Column(Enum("blitz chess", "lightning", "super lightning"), nullable = False)
    White_player = Column(Integer,ForeignKey("users.id"),nullable = False )
    Black_player = Column(Integer,ForeignKey("users.id"), nullable = False)
    Result = Column(Enum("ongoing","White wins", "Black wins", "draw", "abandoned"), default="ongoing")
    LAN = Column(Text, nullable=True)  # Lưu toàn bộ nước đi ở định dạng PGN
    Date = Column(Date, default = datetime.now)

    def calculate_elo(self, result):
        Ra = self.get_elo(self.Type_game, self.White_player)
        Rb = self.get_elo(self.Type_game, self.Black_player)
        Qa = 10**(Ra/400)
        Qb = 10**(Rb/400)
        Ea = Qa/(Qa+Qb)
        Eb = Qb/(Qa+Qb)
        def get_k(elo):
            if elo < 1600:
                return 25
            elif elo < 2000 and elo >= 1600:
                return 20
            elif elo < 2400 and elo >= 2000:
                return 15
            else:
                return 10
        
        if result == "White wins":
            Ka = get_k(self.get_elo(self.Type_game, self.White_player))
            new_Ra = Ra + Ka*(1 - Ea) 
            Kb = get_k(self.get_elo(self.Type_game, self.Black_player))
            new_Rb = Rb + Kb*(0 - Eb)
        elif result == "Black wins":
            Ka = get_k(self.get_elo(self.Type_game, self.White_player))
            new_Ra = Ra + Ka*(0 - Ea) 
            Kb = get_k(self.get_elo(self.Type_game, self.Black_player))
            new_Rb = Rb + Kb*(1 - Eb)
        elif result == "draw":
            Ka = get_k(self.get_elo(self.Type_game, self.White_player))
            new_Ra = Ra + Ka*(0.5 - Ea) 
            Kb = get_k(self.get_elo(self.Type_game, self.Black_player))
            new_Rb = Rb + Kb*(0.5 - Eb)
        elif result == "abandoned":
            pass
        
    def get_elo(self, Type_game, ID_player):
        pass

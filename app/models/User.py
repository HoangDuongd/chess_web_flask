from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import Base




class User(Base):
    # this User class inherits from base class that developed from sqlalchemy -> do not need __init__ function 
    __tablename__ = 'users'
    id  = Column(Integer, unique = True,  primary_key = True)
    username = Column(String(80),unique=False,  nullable = False)
    email = Column(String(120), unique = True, nullable = False)
    password_hash = Column(String(120))
    role = Column(String(20), default='user')
    is_activate = Column(Boolean, default = True)

    def set_password(self, password):
        """Mã hóa mật khẩu"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Kiểm tra mật khẩu"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        """Kiểm tra quyền của user"""
        return self.role == role
    
    def is_admin(self):
        """Kiểm tra có phải admin không"""
        return self.role == 'admin'
    

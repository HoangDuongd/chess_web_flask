from flask import Blueprint, request, jsonify, url_for, session
from app.db import SessionLocal
from app.models.User import User
import string
user_bp = Blueprint("User_routes", __name__)


@user_bp.route("/api/register_user", methods=["POST"])
def create_user():
    db = SessionLocal()
    try:
        data = request.get_json()
        if check_username(data["username"]):
            if data["password"] != data["confirm_password"]:
                return jsonify({"message": "Mật khẩu không khớp"}), 400
            user = User(username=data["username"], email=data["email"])
            user.set_password(data["password"])  # <--- Gọi hàm này để mã hóa mật khẩu

            db.add(user)
            db.commit()
            return jsonify({"message": "User created!"}), 201
        else:
            return jsonify({"error": "Invalid username"}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/api/login", methods=["POST"])
def login():
    db = SessionLocal()
    try:
        data = request.get_json()
        if '@' in data["login_id"]:
            user = db.query(User).filter_by(email=data["login_id"]).first()
        else:  
            user = db.query(User).filter_by(username=data["login_id"]).first()

        if user and user.check_password(data["password"]):
            # Lưu user_id vào session
            session["user_id"] = user.id  
            session.permanent = True  # Cho phép session có hạn dùng
            return jsonify({"message": "Đăng nhập thành công!", "redirect_url": url_for("home")}), 200 # redirect_url return the result is link of home page
        return jsonify({"error": "Sai tên đăng nhập hoặc mật khẩu"}), 401
    finally:
        db.close()


def check_username(username ):
    punctuation = string.punctuation
    for char in username:
        if char.isspace():
            return False
        elif not char.isascii():
            return False
        elif char in punctuation:
            return False
    return True
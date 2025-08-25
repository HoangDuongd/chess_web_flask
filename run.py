from app import create_app ### import from internal file in app folder (__init__ file)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.db import SessionLocal
from app.models.User import User
app = create_app()


@app.route("/login-page")
def login_page():
    return render_template("login_register.html")

@app.route("/")
def index():
    db = SessionLocal()
    try:
        user_id = session.get("user_id") 
        #trong cookie lưu trữ dữ liệu như dạng dictionary, có key và value cookie có bộ nhớ rất ít, 
        # lưu trữ thông tin đăng nhập, ví dụ như 1 bản ghi duy nhất  khi gọi session["user_id"], 
        # nó sẽ tìm xem có key user_id không, nếu có, nó trả về user_id của ngừoi dùng trình duyệt này. nếu không -> none
        if not user_id:
            return redirect(url_for("login_page"))
        user = db.get(User, user_id)
        return render_template("index.html")
    finally:
        db.close()
    


@app.route("/home")
def home():
    db = SessionLocal()
    try:
        user_id = session.get("user_id")
        #trong cookie lưu trữ dữ liệu như dạng dictionary, có key và value cookie có bộ nhớ rất ít, 
        # lưu trữ thông tin đăng nhập, ví dụ như 1 bản ghi duy nhất  khi gọi session["user_id"], 
        # nó sẽ tìm xem có key user_id không, nếu có, nó trả về user_id của ngừoi dùng trình duyệt này. nếu không -> none
        if not user_id:
            return redirect(url_for("login_page"))
        user = db.get(User, user_id)
        return render_template("home.html")
    finally:
        db.close()



@app.route("/member/<username>")
def member():
    db = SessionLocal()
    try:
        user_id = session.get("user_id")
        #trong cookie lưu trữ dữ liệu như dạng dictionary, có key và value cookie có bộ nhớ rất ít, 
        # lưu trữ thông tin đăng nhập, ví dụ như 1 bản ghi duy nhất  khi gọi session["user_id"], 
        # nó sẽ tìm xem có key user_id không, nếu có, nó trả về user_id của ngừoi dùng trình duyệt này. nếu không -> none
        if not user_id:
            return redirect(url_for("login_page"))
        user = db.get(User, user_id)
        return render_template("member.html")
    finally:
        db.close()
    


if __name__ == "__main__":
    app.run(debug=True)
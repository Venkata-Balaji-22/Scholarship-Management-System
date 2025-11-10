from flask import Flask, render_template, request, redirect, make_response, url_for
from passlib.hash import bcrypt_sha256
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta

from shared.db import Base, engine, SessionLocal
from shared.models import User
from shared.config import SECRET_KEY, JWT_SECRET, FLASK_PORT

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Ensure tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return redirect(url_for("ui"))

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if not user or not bcrypt_sha256.verify(password, user.password_hash):
            return render_template("login.html", error="Invalid credentials")
    token = jwt.encode({
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=4)
    }, JWT_SECRET, algorithm="HS256")
    resp = make_response(redirect("/success"))
    resp.set_cookie("access_token", token, httponly=True, samesite="Lax")
    # JS-readable copy for the SPA to include as Authorization when calling FastAPI (demo only)
    resp.set_cookie("access_token_js", token, httponly=False, samesite="Lax")
    return resp

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not name or not email or not password:
        return render_template("register.html", error="All fields are required")

    with SessionLocal() as db:
        if db.query(User).filter(User.email == email).first():
            return render_template("register.html", error="Email already registered")
        user = User(name=name, email=email, password_hash=bcrypt_sha256.hash(password))
        db.add(user)
        db.commit()
    return redirect(url_for("login"))

@app.get("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("access_token_js")
    return resp

@app.get("/success")
def success():
    return "Logged in. You can close this tab and use the Scholarship Finder UI."

# Serve frontend UI
@app.get("/ui")
def ui():
    # Serve the static frontend index
    from flask import send_from_directory
    return send_from_directory("..\\frontend", "index.html")

@app.get("/ui/<path:path>")
def ui_assets(path: str):
    from flask import send_from_directory
    return send_from_directory("..\\frontend", path)

if __name__ == "__main__":
    app.run(port=FLASK_PORT, debug=True)

import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Username / password salah", "danger")
            return redirect(url_for("auth.login"))

        # SET SESSION
        session["user_id"] = user.id
        session["username"] = user.username
        session["is_admin"] = user.is_admin

        flash("Login berhasil", "success")

        # 🔥 INI KUNCINYA
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("public.home"))

    return render_template("login.html")



@bp.route("/logout")
def logout():
    session.clear()
    flash("Logout berhasil", "success")
    return redirect(url_for("public.home"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username dan password wajib diisi.", "warning")
            return redirect(url_for("auth.register"))

        exists = User.query.filter_by(username=username).first()
        if exists:
            flash("Username sudah dipakai.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            password_hash=password,
            is_admin=False
        )

        from app.extensions import db
        db.session.add(user)
        db.session.commit()

        flash("Register berhasil. Silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")





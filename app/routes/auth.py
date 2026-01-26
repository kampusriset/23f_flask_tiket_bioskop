import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("auth", __name__)

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

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password_hash=hashed_password,
            is_admin=False
        )

        from app.extensions import db
        db.session.add(user)
        db.session.commit()

        flash("Register berhasil. Silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")




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





# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.service.user_service import UserService
from app.exceptions import ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            UserService.register_user(request.form.to_dict())
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))
        except ValidationError as e:
            flash(str(e), "error")

    return render_template("auth_register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = UserService.authenticate(
            request.form.get("username"),  # ✅ FIXED
            request.form.get("password")
        )
        if user:
            session["user_id"] = user.id
            session["username"] = user.username  # ✅ FIXED
            flash("Login successful.", "success")
            return redirect(url_for("tasks.list_tasks_page"))

        flash("Invalid username or password.", "error")

    return render_template("auth_login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))

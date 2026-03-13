from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.forms.auth_forms import LoginForm, RegisterForm
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Inicio de sesión correcto")
            return redirect(url_for("public.home"))

        flash("Credenciales incorrectas")

    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Ya existe una cuenta con ese email")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            role="user"
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Cuenta creada correctamente. Ya podés iniciar sesión.")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for("public.home"))
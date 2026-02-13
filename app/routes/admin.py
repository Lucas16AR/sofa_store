import cloudinary.uploader
from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from app.models import OptionCategory, Option
from app.extensions import db
from app.forms.admin_forms import CategoryForm, OptionForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    if current_user.role != "admin":
        abort(403)


@admin_bp.route("/")
@login_required
def dashboard():
    admin_required()
    return render_template("admin_dashboard.html")


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    admin_required()

    form = CategoryForm()
    categories = OptionCategory.query.all()

    if form.validate_on_submit():
        existing = OptionCategory.query.filter_by(name=form.name.data).first()
        if existing:
            flash("La categoría ya existe")
        else:
            category = OptionCategory(name=form.name.data)
            db.session.add(category)
            db.session.commit()
            flash("Categoría creada correctamente")
            return redirect(url_for("admin.manage_categories"))

    return render_template("admin_categories.html", form=form, categories=categories)

@admin_bp.route("/options", methods=["GET", "POST"])
@login_required
def manage_options():
    admin_required()

    form = OptionForm()
    form.category.choices = [
        (c.id, c.name) for c in OptionCategory.query.all()
    ]

    options = Option.query.all()

    if form.validate_on_submit():
        image_url = None

        if form.image.data:
            upload_result = cloudinary.uploader.upload(form.image.data)
            image_url = upload_result["secure_url"]

        option = Option(
            name=form.name.data,
            category_id=form.category.data,
            image_url=image_url
        )

        db.session.add(option)
        db.session.commit()

        flash("Opción creada correctamente")
        return redirect(url_for("admin.manage_options"))

    return render_template("admin_options.html", form=form, options=options)
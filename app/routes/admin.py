import cloudinary.uploader
from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user

from app.models import OptionCategory, Option, Product, Order
from app.extensions import db
from app.forms.admin_forms import CategoryForm, OptionForm, ProductForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    if current_user.role != "admin":
        abort(403)


@admin_bp.route("/")
@login_required
def dashboard():
    admin_required()

    total_categories = OptionCategory.query.count()
    total_options = Option.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()

    return render_template(
        "admin_dashboard.html",
        total_categories=total_categories,
        total_options=total_options,
        total_products=total_products,
        total_orders=total_orders
    )


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    admin_required()

    form = CategoryForm()
    categories = OptionCategory.query.order_by(OptionCategory.created_at.desc()).all()

    if form.validate_on_submit():
        existing = OptionCategory.query.filter_by(name=form.name.data.strip()).first()

        if existing:
            flash("La categoría ya existe")
        else:
            category = OptionCategory(name=form.name.data.strip())
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
        (c.id, c.name) for c in OptionCategory.query.order_by(OptionCategory.name.asc()).all()
    ]

    options = Option.query.order_by(Option.created_at.desc()).all()

    if form.validate_on_submit():
        image_url = None

        if form.image.data:
            upload_result = cloudinary.uploader.upload(form.image.data)
            image_url = upload_result["secure_url"]

        option = Option(
            name=form.name.data.strip(),
            category_id=form.category.data,
            image_url=image_url,
            is_active=True
        )

        db.session.add(option)
        db.session.commit()

        flash("Opción creada correctamente")
        return redirect(url_for("admin.manage_options"))

    return render_template("admin_options.html", form=form, options=options)


@admin_bp.route("/products", methods=["GET", "POST"])
@login_required
def manage_products():
    admin_required()

    form = ProductForm()
    products = Product.query.order_by(Product.created_at.desc()).all()

    if form.validate_on_submit():
        image_url = form.image_url.data.strip() if form.image_url.data else None

        product = Product(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            base_price=form.base_price.data,
            image_url=image_url,
            is_active=True
        )

        db.session.add(product)
        db.session.commit()

        flash("Producto creado correctamente")
        return redirect(url_for("admin.manage_products"))

    return render_template("admin_products.html", form=form, products=products)


@admin_bp.route("/orders")
@login_required
def manage_orders():
    admin_required()

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_orders.html", orders=orders)
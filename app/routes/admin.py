import os
import cloudinary.uploader
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user

from app.models import OptionCategory, Option, Product, Order
from app.extensions import db
from app.forms.admin_forms import CategoryForm, OptionForm, ProductForm, SimpleSubmitForm

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
    delete_form = SimpleSubmitForm()
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

    return render_template(
        "admin_categories.html",
        form=form,
        categories=categories,
        delete_form=delete_form
    )

@admin_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    admin_required()

    category = OptionCategory.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        new_name = form.name.data.strip()
        existing = OptionCategory.query.filter(
            OptionCategory.name == new_name,
            OptionCategory.id != category.id
        ).first()

        if existing:
            flash("Ya existe otra categoría con ese nombre")
        else:
            category.name = new_name
            db.session.commit()
            flash("Categoría actualizada correctamente")
            return redirect(url_for("admin.manage_categories"))

    return render_template("edit_category.html", form=form, category=category)

@admin_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):
    admin_required()

    category = OptionCategory.query.get_or_404(category_id)

    if category.options:
        flash("No se puede borrar una categoría que tiene opciones asociadas")
        return redirect(url_for("admin.manage_categories"))

    db.session.delete(category)
    db.session.commit()
    flash("Categoría eliminada correctamente")
    return redirect(url_for("admin.manage_categories"))

@admin_bp.route("/options", methods=["GET", "POST"])
@login_required
def manage_options():
    admin_required()

    form = OptionForm()
    toggle_form = SimpleSubmitForm()
    delete_form = SimpleSubmitForm()

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
            is_active=True,
            price_modifier=float(form.price_modifier.data or 0)
        )

        db.session.add(option)
        db.session.commit()

        flash("Opción creada correctamente")
        return redirect(url_for("admin.manage_options"))

    return render_template(
        "admin_options.html",
        form=form,
        options=options,
        toggle_form=toggle_form,
        delete_form=delete_form
    )

@admin_bp.route("/options/<int:option_id>/toggle", methods=["POST"])
@login_required
def toggle_option(option_id):
    admin_required()

    option = Option.query.get_or_404(option_id)
    option.is_active = not option.is_active
    db.session.commit()

    if option.is_active:
        flash("Opción activada correctamente")
    else:
        flash("Opción desactivada correctamente")

    return redirect(url_for("admin.manage_options"))

@admin_bp.route("/options/<int:option_id>/delete", methods=["POST"])
@login_required
def delete_option(option_id):
    admin_required()

    option = Option.query.get_or_404(option_id)
    db.session.delete(option)
    db.session.commit()
    flash("Opción eliminada correctamente")
    return redirect(url_for("admin.manage_options"))

@admin_bp.route("/products", methods=["GET", "POST"])
@login_required
def manage_products():
    admin_required()

    form = ProductForm()
    toggle_form = SimpleSubmitForm()
    delete_form = SimpleSubmitForm()
    products = Product.query.order_by(Product.created_at.desc()).all()

    if form.validate_on_submit():
        image_url = None

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            unique_filename = f"{uuid4().hex}_{filename}"

            upload_folder = os.path.join("app", "static", "uploads", "products")
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, unique_filename)
            form.image.data.save(file_path)

            image_url = url_for(
                "static",
                filename=f"uploads/products/{unique_filename}"
            )

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

    return render_template(
        "admin_products.html",
        form=form,
        products=products,
        toggle_form=toggle_form,
        delete_form=delete_form
    )

@admin_bp.route("/products/<int:product_id>/toggle", methods=["POST"])
@login_required
def toggle_product(product_id):
    admin_required()

    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()

    if product.is_active:
        flash("Producto activado correctamente")
    else:
        flash("Producto desactivado correctamente")

    return redirect(url_for("admin.manage_products"))

@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    admin_required()

    product = Product.query.get_or_404(product_id)

    if product.orders:
        flash("No se puede eliminar un producto que ya tiene pedidos asociados. Podés desactivarlo.")
        return redirect(url_for("admin.manage_products"))

    db.session.delete(product)
    db.session.commit()
    flash("Producto eliminado correctamente")
    return redirect(url_for("admin.manage_products"))

@admin_bp.route("/orders")
@login_required
def manage_orders():
    admin_required()

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_orders.html", orders=orders)
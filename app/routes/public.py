from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.public_forms import ConfiguratorForm
from app.models import Product, OptionCategory, Option, Order, OrderConfiguration
from app.extensions import db

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    products = Product.query.filter_by(is_active=True).all()
    return render_template("home.html", products=products)


@public_bp.route("/configurator/<int:product_id>", methods=["GET", "POST"])
@login_required
def configurator(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    categories = OptionCategory.query.all()
    form = ConfiguratorForm()

    if form.validate_on_submit():
        total_price = product.base_price

        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            status="pending",
            total_price=0,
            notes=request.form.get("notes")
        )

        db.session.add(order)
        db.session.flush()

        for category in categories:
            selected_option_id = request.form.get(f"category_{category.id}")

            if selected_option_id:
                option = Option.query.get(int(selected_option_id))

                if option and option.price_modifier:
                    total_price += option.price_modifier

                if option:
                    config = OrderConfiguration(
                        order_id=order.id,
                        option_id=option.id,
                        option_name_snapshot=option.name,
                        option_price_snapshot=option.price_modifier or 0
                    )
                    db.session.add(config)

        order.total_price = total_price
        db.session.commit()

        flash("Pedido realizado correctamente")
        return redirect(url_for("public.my_orders"))

    return render_template(
        "configurator.html",
        product=product,
        categories=categories,
        form=form
    )


@public_bp.route("/my-orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("my_orders.html", orders=orders)
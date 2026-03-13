from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.public_forms import ConfiguratorForm
from app.models import Product, OptionCategory, Option, Order, OrderConfiguration
from app.extensions import db
from urllib.parse import quote

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
            notes=request.form.get("notes"),
            customer_name=current_user.name,
            customer_email=current_user.email,
            customer_phone=current_user.phone
        )

        db.session.add(order)
        db.session.flush()

        for category in categories:
            selected_option_id = request.form.get(f"category_{category.id}")

            if selected_option_id:
                option = Option.query.filter_by(
                    id=int(selected_option_id),
                    is_active=True
                ).first()

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
        return redirect(url_for("public.order_success", order_id=order.id))

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

@public_bp.route("/order-success/<int:order_id>")
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template("order_success.html", order=order)

@public_bp.route("/order-whatsapp/<int:order_id>")
@login_required
def order_whatsapp(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()

    phone_number = "5492604647804"  # Cambiar por el número real del negocio

    message_lines = [
        "Hola, quiero consultar por este pedido:",
        f"Pedido #{order.id}",
        f"Cliente: {order.customer_name}",
        f"Email: {order.customer_email}",
        f"Teléfono: {order.customer_phone or 'No informado'}",
        f"Producto: {order.product.name}",
        f"Fecha: {order.created_at.strftime('%d/%m/%Y %H:%M')}",
        "Configuración:"
    ]

    for config in order.configurations:
        if config.option_price_snapshot:
            message_lines.append(f"- {config.option_name_snapshot} (${config.option_price_snapshot})")
        else:
            message_lines.append(f"- {config.option_name_snapshot}")

    message_lines.append(f"Total: ${order.total_price}")

    if order.notes:
        message_lines.append(f"Observaciones: {order.notes}")

    message = "\n".join(message_lines)
    whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"

    return redirect(whatsapp_url)
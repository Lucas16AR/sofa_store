from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import OptionCategory, Order, OrderConfiguration
from app.extensions import db
from app.forms.public_forms import ConfiguratorForm

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    return render_template("home.html")

@public_bp.route("/configurator", methods=["GET", "POST"])
@login_required
def configurator():
    categories = OptionCategory.query.all()
    form = ConfiguratorForm()

    if form.validate_on_submit():
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.flush()

        for category in categories:
            selected_option_id = request.form.get(f"category_{category.id}")
            if selected_option_id:
                config = OrderConfiguration(
                    order_id=order.id,
                    option_id=int(selected_option_id)
                )
                db.session.add(config)

        db.session.commit()
        flash("Pedido guardado correctamente")
        return redirect(url_for("public.home"))

    return render_template("configurator.html", categories=categories, form=form)
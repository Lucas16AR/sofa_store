from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import abort

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():
    if current_user.role != "admin":
        abort(403)

    return render_template("admin_dashboard.html")
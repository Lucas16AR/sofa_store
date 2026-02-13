from flask import Flask
from .extensions import db, login_manager, migrate
from .models import User
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.public import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()

    return app


def create_admin_if_not_exists():
    if not User.query.filter_by(role="admin").first():
        admin = User(
            email="admin@sofastore.com",
            role="admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin creado automáticamente")
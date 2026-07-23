from flask import Flask, redirect, url_for

from .config import Config
from .extensions import db, login_manager, migrate


def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from . import models  # noqa: F401
    from .seed import seed_demo_data

    from .blueprints.auth.routes import auth_bp
    from .blueprints.companies.routes import companies_bp
    from .blueprints.contacts.routes import contacts_bp
    from .blueprints.deals.routes import deals_bp
    from .blueprints.activities.routes import activities_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(companies_bp, url_prefix="/companies")
    app.register_blueprint(contacts_bp, url_prefix="/contacts")
    app.register_blueprint(deals_bp, url_prefix="/deals")
    app.register_blueprint(activities_bp, url_prefix="/activities")

    @app.route("/")
    def index():
        return redirect(url_for("deals.index"))

    @app.cli.command("seed-demo")
    def seed_demo_command():
        """Seed demo data for the capstone dataset."""
        db.create_all()
        seed_demo_data()

    @app.cli.command("init-db")
    def init_db_command():
        """Create all database tables for a fresh environment."""
        db.create_all()

    return app

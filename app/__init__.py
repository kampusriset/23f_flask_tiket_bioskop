from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema.db'

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.public import bp as public_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.admin import bp as admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)

    # 🔹 AUTO SEED
    from app.seed import run_seed
    with app.app_context():
        run_seed()

    return app

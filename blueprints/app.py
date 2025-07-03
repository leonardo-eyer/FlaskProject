from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "tutorial.db"

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = "unsafekey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_NAME
    db.init_app(app)

    from blueprints.views.routes import views
    from blueprints.auth.routes import auth
    from blueprints.core.routes import core

    app.register_blueprint(views, url_prefix="/views")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(core, url_prefix="")

    from blueprints.auth.models import User
    from blueprints.core.models import Note

    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        db.create_all()
        print("Database created successfully")
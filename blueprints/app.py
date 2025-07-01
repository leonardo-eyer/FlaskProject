from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = "unsafekey"

    from blueprints.views.routes import views
    from blueprints.auth.routes import auth
    from blueprints.core.routes import core

    app.register_blueprint(views, url_prefix="/views")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(core, url_prefix="")

    return app


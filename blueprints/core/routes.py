from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user

core = Blueprint("core", __name__, template_folder="templates")

@core.route('/')
@login_required
def index():
    return render_template("index.html", user=current_user)
from flask import Blueprint

core = Blueprint("core", __name__)

@core.route('/')
def index():
    return "<h1>Test core</h1>"
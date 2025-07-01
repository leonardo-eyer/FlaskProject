from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route('/')
def index():
    return "<h1>Test auth</h1>"
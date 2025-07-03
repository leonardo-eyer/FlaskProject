from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from blueprints.app import db
import json

core = Blueprint("core", __name__, template_folder="templates")

@core.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        note = request.form["note"]
        if len(note) <1:
            flash("note is too short", category="error")
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("new note created", category="success")
    return render_template("index.html", user=current_user)

@core.route("delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["noteId"]
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})
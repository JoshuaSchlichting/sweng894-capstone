import os

from flask import render_template, send_from_directory
from flask_jwt_extended.view_decorators import jwt_required

from main import app


@app.route("/index.html")
@app.route("/index")
@app.route("/")
def index():
    user = None
    return render_template("index.html.jinja", user=user)


@app.route("/login", methods=["GET"])
def get_login_page():
    return render_template("login.html.jinja")


@app.route("/create_user.html", methods=["GET"])
def get_create_new_user_page():
    return render_template("create_new_user.html.jinja")


@app.route("/create_election.html", methods=["GET"])
def get_create_new_election_page():
    return render_template("create_election.html.jinja")


@app.route("/add_candidate_to_election.html", methods=["GET"])
@jwt_required()
def get_add_candidate_to_election_page():
    return render_template("add_candidate_to_election.html.jinja")


@app.route("/elections.html", methods=["GET"])
def get_election_view():
    return render_template("elections.html.jinja")


@app.route("/static/js/<path:path>")
def serve_static_js(path):
    """Serve static js files"""
    THIS_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(THIS_MODULE_DIR, "static", "js"), path)


@app.route("/static/css/<path:path>")
def serve_static_css(path):
    """Serve static css files"""
    THIS_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(THIS_MODULE_DIR, "static", "css"), path)

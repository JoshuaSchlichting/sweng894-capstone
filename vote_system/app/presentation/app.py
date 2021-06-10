from datetime import datetime, timedelta

from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from loguru import logger
from werkzeug.security import generate_password_hash, check_password_hash

from core import ApiFactory
from core import AbstractDataAccessLayer


app = Flask(__name__)
SECRET_KEY = "change this for production"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)


def _get_data_access_layer() -> AbstractDataAccessLayer:
    logger.warning("Using mocked up data access layer - you are OFFLINE!!!")
    from unittest.mock import Mock

    dal = Mock(spec=AbstractDataAccessLayer)
    dal.create_user.return_value = 3456
    dal.cast_vote.return_value = 1234
    dal.create_candidate.return_value = 83445
    return dal


def _get_api_factory(token: dict):
    dal = _get_data_access_layer()
    return ApiFactory(token=token, data_access_layer=dal, logger=logger)


@app.route("/")
def index():
    return "SUCCESS"


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# signup route
@app.route("/signup", methods=["POST"])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")

    # checking for existing user
    user = User.query.filter_by(email=email).first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password),
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response("Successfully registered.", 201)
    else:
        # returns 202 if user already exists
        return make_response("User already exists. Please Log in.", 202)


@app.route("/user", methods=["POST"])
@jwt_required()
def create_user():
    admin_api = _get_api_factory(None).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.json["username"])
    return jsonify({"userId": newly_create_user_id})


@app.route("/election", methods=["POST"])
@jwt_required()
def create_election(token):

    admin_api = ApiFactory(
        token=None, data_access_layer=None, logger=logger
    ).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})


@app.route("/vote", methods=["POST"])
@jwt_required()
def create_vote():

    voter_api = _get_api_factory(None).create_voter_api()
    newly_create_user_id = voter_api.cast_vote(
        user_id=request.json["userId"],
        election_id=request.json["electionId"],
        ranked_candidate_list=request.json["rankedCandidateList"],
    )
    return jsonify({"userId": newly_create_user_id})


@app.route("/candidate", methods=["POST"])
@jwt_required()
def create_candidate():

    admin_api = ApiFactory(
        token=None, data_access_layer=None, logger=logger
    ).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})

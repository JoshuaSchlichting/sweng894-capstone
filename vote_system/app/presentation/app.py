from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended.utils import get_jwt_header
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from loguru import logger
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

from core import ApiFactory
from core import AbstractDataAccessLayer, UserFactory


app = Flask(__name__, static_url_path="/static")
SECRET_KEY = "change this for production"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)
from . import (
    views,
)  # noqa This is necessary for routes outside of this file, after app is created.


def _get_data_access_layer() -> AbstractDataAccessLayer:
    import db_implementation

    db = db_implementation.MongoDbApi(MongoClient())
    return db


def _get_api_factory(user_id: int):
    dal = _get_data_access_layer()
    return ApiFactory(user_id=user_id, data_access_layer=dal, logger=logger)


def _get_user_factory(logger) -> UserFactory:
    return UserFactory(data_access_layer=_get_data_access_layer(), logger=logger)


@app.route("/login", methods=["POST"])
def login():
    logger.info(str(request))
    username = request.form.get("inputUsername")
    password = request.form.get("inputPassword")
    dal = _get_data_access_layer()
    if not dal.get_user_is_valid(username=username, password=password):
        return jsonify({"msg": "Bad username or password"}), 401

    user_info = dal.get_user_info_by_name(username)

    access_token = create_access_token(
        identity=user_info["id"],
        additional_claims={
            "userType": user_info["user_type"],
            "username": user_info["username"],
        },
    )

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

    current_user_id = get_jwt_identity()
    admin_api = _get_api_factory(user_id=current_user_id).create_admin_api()
    newly_create_user_id = admin_api.create_user(
        username=request.json["username"],
        password=request.json.get("password"),
        user_type=request.json["userType"],
    )
    user_info = _get_data_access_layer().get_user_info_by_id(newly_create_user_id)
    return jsonify(
        {
            "userId": newly_create_user_id,
            "username": user_info["username"],
            "userType": user_info["user_type"],
        }
    )


@app.route("/election", methods=["POST"])
@jwt_required()
def create_election():
    header = get_jwt_header()
    logger.debug("HEADER" + str(header))
    logger.debug(request.json)
    admin_api = _get_api_factory(get_jwt_identity()).create_admin_api()
    election_id = ""
    try:
        election_id = admin_api.create_election(
            election_name=request.json.get("electionName"),
            start_date=request.json.get("startDate"),
            end_date=request.json.get("endDate"),
        )
    except Exception as e:
        return jsonify({"msg": str(e)})
    return jsonify({"msg": "Election created. ID: " + election_id})


@app.route("/election/all", methods=["GET"])
def get_all_elections():
    basic_api = _get_api_factory(None).create_basic_api()
    return jsonify(basic_api.get_all_elections())


@app.route("/election", methods=["GET"])
def get_election():
    basic_api = _get_api_factory(None).create_basic_api()
    return jsonify(basic_api.get_election(request.json["electionId"]))


@app.route("/election/candidate", methods=["POST"])
@jwt_required()
def add_candidate_to_election():
    admin_api = _get_api_factory(get_jwt_identity()).create_admin_api()
    return jsonify(
        admin_api.add_candidate_to_election(
            election_id=request.json["electionId"],
            candidate_id=request.json["candidateId"],
        )
    )

@app.route("/election/candidate", methods=["GET"])
def get_candidates_by_election():
    basic_api = _get_api_factory(None).create_basic_api()
    return jsonify(
        basic_api.get_candidates_by_election(election_id=request.args.get("electionId"))
    )

@app.route("/vote", methods=["POST"])
@jwt_required()
def create_vote():
    voter_api = _get_api_factory(None).create_voter_api()
    new_vote_id = voter_api.cast_vote(
        user_id=request.json["userId"],
        election_id=request.json["electionId"],
        ranked_candidate_list=request.json["rankedCandidateList"],
    )
    return jsonify({"userId": new_vote_id})


@app.route("/candidate", methods=["POST"])
@jwt_required()
def create_candidate():
    admin_api = _get_api_factory(None).create_admin_api()
    newly_create_user_id = admin_api.create_candidate(username=request.json["username"])
    return jsonify({"userId": newly_create_user_id})

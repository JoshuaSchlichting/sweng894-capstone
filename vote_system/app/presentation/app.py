from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify, make_response
from loguru import logger
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from ..core import ApiFactory
from ..core import AbstractDataAccessLayer


app = Flask(__name__)
SECRET_KEY = "change this for production"
app.config["SECRET_KEY"] = SECRET_KEY


def _get_data_access_layer() -> AbstractDataAccessLayer:
    logger.warning("Using mocked up data access layer - you are OFFLINE!!!")
    from unittest.mock import Mock

    return Mock(spec=AbstractDataAccessLayer)


def _get_api_factory(token: dict):
    dal = _get_data_access_layer()
    return ApiFactory(token=token, data_access_layer=dal, logger=logger)


def token_required(f):
    """decorator for verifying the JWT"""

    def func(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401
        try:
            # decoding the payload to fetch the stored details
            token_dict = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        return f(token_dict, *args, **kwargs)

    return func


# route for loging user in
@app.route("/login", methods=["POST"])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get("email") or not auth.get("password"):
        # returns 401 if any email or / and password is missing
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
        )

    user = User.query.filter_by(email=auth.get("email")).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
        )

    if check_password_hash(user.password, auth.get("password")):
        # generates the JWT Token
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )

        return make_response(jsonify({"token": token.decode("UTF-8")}), 201)
    # returns 403 if password is wrong
    return make_response(
        "Could not verify",
        403,
        {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
    )


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
def create_user(token):

    admin_api = _get_api_factory(token).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})


@app.route("/election", methods=["POST"])
def create_election(token):

    admin_api = ApiFactory(
        token=None, data_access_layer=None, logger=logger
    ).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})


@app.route("/user", methods=["POST"])
def create_user():

    admin_api = ApiFactory(
        token=None, data_access_layer=None, logger=logger
    ).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})


@app.route("/user", methods=["POST"])
def create_user():

    admin_api = ApiFactory(
        token=None, data_access_layer=None, logger=logger
    ).create_admin_api()
    newly_create_user_id = admin_api.create_user(username=request.values["username"])
    return jsonify({"userId": newly_create_user_id})


if __name__ == "__main__":
    app.run(debug=True)

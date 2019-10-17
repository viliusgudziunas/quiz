from flask import Blueprint, request, jsonify
from sqlalchemy import exc, or_
from project import db, bcrypt
from project.api.models import User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload"
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        user = User.query.filter(
            or_(User.username == username,
                User.email == User.email == email)).first()
        if user:
            response_object["message"] = "Sorry. That user already exists"
            return jsonify(response_object), 400
        new_user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        auth_token = new_user.encode_auth_token(new_user.id)
        response_object["status"] = "success"
        response_object["message"] = "Successfully registered"
        response_object["auth_token"] = auth_token.decode()
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_object), 400


@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload"
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            response_object["message"] = "User does not exist"
            return jsonify(response_object), 404
        if not password or \
                not bcrypt.check_password_hash(user.password, password):
            response_object["message"] = "Incorrect password"
            return jsonify(response_object), 400
        auth_token = user.encode_auth_token(user.id)
        response_object["status"] = "success"
        response_object["message"] = "Successfully logged in"
        response_object["auth_token"] = auth_token.decode()
        return jsonify(response_object), 200
    except Exception:
        response_object["message"] = "Try again"
        return jsonify(response_object), 500


@auth_blueprint.route("/logout", methods=["GET"])
def logout_user():
    auth_header = request.headers.get("Authorization")
    response_object = {
        "status": "fail",
        "message": "Provide a valid auth token"
    }
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return jsonify(response_object), 401
        response_object["status"] = "success"
        response_object["message"] = "Successfully logged out"
        return jsonify(response_object), 200
    else:
        return jsonify(response_object), 403


@auth_blueprint.route("/status", methods=["GET"])
def get_user_status():
    auth_header = request.headers.get("Authorization")
    response_object = {
        "status": "fail",
        "message": "Provide a valid auth token"
    }
    if not auth_header:
        return jsonify(response_object), 401
    auth_token = auth_header.split(" ")[1]
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str):
        user = User.query.filter_by(id=resp).first()
        response_object["status"] = "success"
        response_object["message"] = "Success"
        response_object["data"] = user.to_json()
        return jsonify(response_object), 200
    response_object["message"] = resp
    return jsonify(response_object), 401

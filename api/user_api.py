import json
import os
import shutil
from datetime import datetime, timedelta, timezone
from logging import ERROR, INFO

import bcrypt
import jwt
from bson.json_util import dumps, loads
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from constants import API, MAX_FILE_LENGTH, UPLOAD_FOLDER
from database import mongodb
from database.serializers import UserSchema
from middleware import authmiddleware
from utils import allowed_file, getUniqueFileName
from utils.exception import CustomException
from utils.logger import log

user_bp = Blueprint("user", __name__)


@user_bp.route(API.USER.LOGIN, methods=["POST"])
def login():
    """API for handle login"""
    try:
        body = request.get_json()
        if "username" not in body:
            raise Exception("username must be provided!")
        if "password" not in body:
            raise Exception("password must be provided!")

        exist = mongodb.collections["users"].find_one({"username": body["username"]})

        if not exist:
            raise Exception("user is not existed!")
        password = body["password"]
        hashed_password = exist["password"]

        # Check password
        if not bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            raise Exception("password is incorrect!")

        # Gen token
        body["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=3 * 60 * 60)
        token = jwt.encode(body, os.environ["JWT_SECRET"])

        user_info = UserSchema().dump(exist)
        user_info.pop("password")

        log(INFO, f"User {user_info} logged in")

        return jsonify({"code": 200, "token": token, "data": user_info})

    except Exception as e:
        log(ERROR, str(e))
        return jsonify({"code": 500, "message": str(e)})


@user_bp.route(API.USER.SIGNUP, methods=["POST"])
def signup():
    """API for handle signup"""

    try:
        body = request.get_json()

        if "username" not in body:
            raise Exception("username must be provided!")
        if "password" not in body:
            raise Exception("password must be provided!")

        exist = mongodb.collections["users"].find_one({"username": body["username"]})

        if exist:
            raise Exception("username has been existed!")

        hash_password = bcrypt.hashpw(
            body["password"].encode("utf-8"), bcrypt.gensalt()
        )
        body["password"] = hash_password.decode("utf-8")

        res = mongodb.collections["users"].insert_one(body)
        _id = res.inserted_id

        info = mongodb.collections["users"].find_one({"_id": _id})
        info = UserSchema().dump(info)
        info.pop("password")

        return jsonify({"code": 200, "message": "Signup success", "data": info})
    except Exception as e:
        log(ERROR, str(e))
        return jsonify({"code": 500, "message": str(e)})


@user_bp.route(API.USER.ME, methods=["GET"])
@authmiddleware
def get_info(current_user):
    """API for handle login"""
    try:
        current_user = UserSchema().dump(current_user)
        current_user.pop("password")
        return jsonify({"code": 200, "data": current_user})

    except Exception as e:
        log(ERROR, str(e))
        return jsonify({"code": 500, "message": str(e)})


@user_bp.route(API.USER.LOGOUT, methods=["POST"])
@authmiddleware
def logout(current_user):
    """API for handle logout"""
    try:
        current_user = UserSchema().dump(current_user)

        saved_model = f"weights/{current_user['_id']}"

        if os.path.exists(saved_model):
            shutil.rmtree(saved_model)

        return jsonify({"code": 200, "data": "Success logout"})

    except Exception as e:
        log(ERROR, str(e))
        return jsonify({"code": 500, "message": str(e)})


@user_bp.route(API.USER.UPLOAD, methods=["POST"])
@authmiddleware
def upload(current_user):
    """API for handle upload"""
    try:
        if "file" not in request.files:
            raise CustomException(status_code=400, message="No file part!")

        file = request.files["file"]

        if file.filename == "":
            raise CustomException(status_code=400, message="No selected file!")

        if not allowed_file(file.filename):
            raise CustomException(status_code=400, message="File type not allowed!")

        filename = secure_filename(file.filename)
        saved_folder = getUniqueFileName(UPLOAD_FOLDER)

        if not os.path.exists(saved_folder):
            os.makedirs(saved_folder)

        filepath = os.path.join(saved_folder, filename)

        print(filepath)
        file.save(filepath)

        return jsonify({"code": 200, "data": "Success upload"})

    except Exception as e:
        print(e)
        log(ERROR, str(e))
        return jsonify({"code": e.status_code or 500, "message": str(e)})

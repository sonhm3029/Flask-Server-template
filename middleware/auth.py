import os
from functools import wraps
from logging import INFO

import bcrypt
import jwt
from flask import abort, request

from database import mongodb
from utils.logger import log


def token_required(f):
    @wraps(f)
    def decorated(*args, **kawargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
                "code": 401,
            }, 401
        try:
            data = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
            if not data.get("username") or not data.get("password"):
                return {"message": "Invalid authorization!", "code": 401}, 401
            current_user = mongodb.collections["users"].find_one(
                {"username": data["username"]}
            )
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                    "code": 401,
                }, 401

            true_pwd = current_user.get("password")
            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), true_pwd.encode("utf-8")
            ):
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                    "code": 401,
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "code": 500,
            }, 500

        return f(current_user, *args, *kawargs)

    return decorated

#!/usr/bin/env python3
"""Session Auth Endpints"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login endpoint"""
    email = request.form.get("email")
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    new_session = auth.create_session(user.id)
    sessioname = getenv("SESSION_NAME")
    res = jsonify(user.to_json())
    res.set_cookie(sessioname, new_session)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """logs out user"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200

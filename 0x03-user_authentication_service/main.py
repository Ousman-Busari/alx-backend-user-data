#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """registers a new user"""
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/users', data=payload)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """checks if login fails with wrong password"""
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """logs in a user"""
    payload = {'email': email, 'password': password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """checks if profile fails when user is not logged in"""
    response = requests.get('http://localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """checks if profile works when user is logged in"""
    cookies = {'session_id': session_id}
    response = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """checks if logout works"""
    cookies = {'session_id': session_id}
    response = requests.delete('http://localhost:5000/delete', cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """checks if reset password token works"""
    payload = {'email': email}
    response = requests.post(
        'http://localhost:5000/reset_password', data=payload)
    assert response.status_code == 200
    token = response.json().get('reset_token')
    assert token is not None
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """checks if update password works"""
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
        }
    response = requests.put(
        'http://localhost:5000/reset_password', data=payload)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

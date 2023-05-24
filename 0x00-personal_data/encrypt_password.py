#!/usr/bin/emv python3
"""
encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks is password matched hashed_password,
    returns a boolean
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

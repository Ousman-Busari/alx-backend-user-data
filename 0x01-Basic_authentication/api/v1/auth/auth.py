#!/usr/bin/env python3
"""
auth class
"""
from flask import request
from typing import (List,
                    TypeVar)
import re


class Auth:
    """Authrization class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires authorization"""
        if (path is None) or (excluded_paths is
           None) or len(excluded_paths) == 0:
            return True
        for excl_path in excluded_paths:
            re_compatible_ex_path = excl_path[:-1] + "." + "*"
            if (re.match(re_compatible_ex_path, path)):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the authorization header of a request"""
        if (request is None or "Authorization" not in request.headers):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """determines the current user"""
        return None

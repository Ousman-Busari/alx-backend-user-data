#!/usr/bin/env python3
"""
Basic Auth Class
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar, Tuple


class BasicAuth(Auth):
    """BasicAUth authorization scheme instance"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract authorization values with in base64"""
        if (
           authorization_header is None
           or not isinstance(authorization_header, str)
           or not authorization_header.startswith("Basic ")
           ):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """retursn the decoded value of Base64 string"""
        if (
           base64_authorization_header is None
           or not isinstance(base64_authorization_header, str)
           ):
            return None
        try:
            auth_in_bytes = base64.b64decode(base64_authorization_header)
            return auth_in_bytes.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """
        returns the user email and password from the Base64 decoded value
        """
        if (
           decoded_base64_authorization_header is None
           or not isinstance(decoded_base64_authorization_header, str)
           or ":" not in decoded_base64_authorization_header
           ):
            return (None, None)
        decoded_and_divided = decoded_base64_authorization_header.split(":")
        return (
               decoded_and_divided[0],
               ":".join(decoded_and_divided[1:]),
               )

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        if (
            user_email is None or not isinstance(user_email, str)
            or user_pwd is None or not isinstance(user_pwd, str)
           ):
            return None
        try:
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        auth_encoded_value = self.extract_base64_authorization_header(
                                auth_header)
        auth_decoded_value = self.decode_base64_authorization_header(
                                auth_encoded_value)
        user_creds = self.extract_user_credentials(auth_decoded_value)
        return self.user_object_from_credentials(
            user_email=user_creds[0],
            user_pwd=user_creds[1]
        )

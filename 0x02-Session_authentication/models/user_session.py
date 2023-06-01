#!/usr/bin/env python3
"""user_session module"""
from models.base import Base


class UserSession(Base):
    """"class for storing user session data"""
    def __init__(self, *args: list, **kwargs: dict):
        """initializes user session"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")

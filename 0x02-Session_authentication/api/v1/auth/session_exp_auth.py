#!/usr/bin/env python3
"""Session Exp Auth Class"""
from datetime import datetime, timedelta
from .session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session auth with expiration time"""
    def __init__(self):
        """initialize a new SessionExpAuth instance"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None):
        """creates a new session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """get user id from session id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary.keys():
            return None
        created_at = session_dictionary["created_at"]
        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return session_dictionary["user_id"]
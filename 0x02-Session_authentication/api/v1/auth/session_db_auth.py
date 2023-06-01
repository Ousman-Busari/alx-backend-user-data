#!/usr/bin/env python3
"""
database session authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """database session authentication"""
    def create_session(self, user_id: str = None):
        """creates a session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """gets a user id from a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        UserSession.load_from_file()
        users_sessions = UserSession.search({'session_id': session_id})
        if not users_sessions or len(users_sessions) == 0:
            return None
        user_session = users_sessions[0]
        # session_created_at = user_session.created_at
        session_created_at = self.user_id_by_session_id[session_id]['created_at']
        print(session_created_at)
        expired_time = session_created_at + timedelta(seconds=self.session_duration)
        print(expired_time, " ttt")
        if expired_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request: str = None):
        """deletes users sessionand logout user"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        users_sessions = UserSession.search({'session_id': session_id})
        if not users_sessions:
            return False
        user_session = users_sessions[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
            return True
        except Exception:
            return False

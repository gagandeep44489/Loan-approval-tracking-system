"""Authentication service."""
from __future__ import annotations

from models import UserModel


class AuthService:
    def __init__(self, user_model: UserModel):
        self.user_model = user_model

    def login(self, username: str, password: str):
        if not username.strip() or not password:
            return None, "Username and password are required"

        user = self.user_model.authenticate(username=username, password=password)
        if not user:
            return None, "Invalid credentials"

        return user, "Login successful"

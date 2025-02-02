"""Модуль с ошибками"""

from schemas import base_schemas

class AuthenticationError(Exception):
    """Ошибка авторизации запроса"""
    def __init__(self, token: str, api: str):
        self.token = token
        self.error = base_schemas.BaseErrorSchem(
            name="AuthenticationError",
            details="Invalid access token",
            api=api,
            status_code=401
        )

    def __str__(self):
        return f"Send not valid token -> {self.token}"

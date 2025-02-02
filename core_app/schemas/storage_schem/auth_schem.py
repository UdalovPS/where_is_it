from typing import Union

from pydantic import BaseModel


class AuthSchem(BaseModel):
    """Схема для предоставления данных по аутентификации"""
    id: int
    token: str
    customer_id: int
    name: str

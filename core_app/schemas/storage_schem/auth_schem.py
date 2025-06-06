from typing import Optional
import datetime

from pydantic import BaseModel


class AuthSchem(BaseModel):
    """Схема для предоставления данных по аутентификации"""
    id: int
    token: str
    name: str
    organization_id: int
    branch_id: Optional[int]
    details: Optional[str]
    created_at: datetime.datetime
    update_at: datetime.datetime

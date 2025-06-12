from typing import Optional, Dict
import datetime

from pydantic import BaseModel


class ClientLocationSchem(BaseModel):
    id: int
    branch_id: Optional[int]
    organization_id: int
    created_at: datetime.datetime
    update_at: datetime.datetime


class ClientSchem(BaseModel):
    """Схема для представления данных клиента"""
    id: int
    name: str
    frontend_service_id: int
    frontend_id: int
    frontend_data: Optional[Dict]
    created_at: datetime.datetime
    update_at: datetime.datetime


class ClientWithLocationSchem(ClientSchem):
    location: Optional[ClientLocationSchem] = None


class LocationSchem(BaseModel):
    id: int
    client_id: int
    organization_id: int
    branch_id: Optional[int]

    class Config:
        from_attributes = True



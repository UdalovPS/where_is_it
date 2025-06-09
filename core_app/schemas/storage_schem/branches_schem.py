from typing import Optional, Any, List
import datetime

from pydantic import BaseModel

class ContentSchem(BaseModel):
    """Схема контекста изображения"""
    content_path: Any
    filename: str
    content_type: str
    size: int
    files: List[str]
    file_id: str
    upload_storage: str
    uploaded_at: datetime.datetime
    path: str
    url: str
    saved: bool


class BranchPlanSchemaBase(BaseModel):
    title: str
    branch_id: Optional[int] = None
    organization_id: int
    content: ContentSchem
    exit_x: int
    exit_y: int
    creator_id: Optional[int] = None
    updator_id: Optional[int] = None

    class Config:
        from_attributes = True


class BranchSchemaCreate(BranchPlanSchemaBase):
    pass


class BranchSchemaUpdate(BaseModel):
    title: Optional[str] = None
    branch_id: Optional[int] = None
    organization_id: Optional[int] = None
    content: Optional[Any] = None
    updator_id: Optional[int] = None


class BranchPlanSchema(BranchPlanSchemaBase):
    """Полная схема создания Плана помещения"""
    id: int
    created_at: datetime.datetime
    update_at: datetime.datetime

    class Config:
        from_attributes = True  # Ранее называлось orm_mode=True в Pydantic v1


class BranchSchema(BaseModel):
    id: int
    name: str
    address: str
    city_id: int
    organization_id: int
    latitude: float
    longitude: float

    creator_id: Optional[int]
    updator_id: Optional[int]
    created_at: datetime.datetime
    update_at: datetime.datetime
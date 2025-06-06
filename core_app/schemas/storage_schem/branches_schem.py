from typing import Optional, Any
import datetime

from pydantic import BaseModel

class BranchSchemaBase(BaseModel):
    title: str
    branch_id: Optional[int] = None
    organization_id: int
    content: Any  # Для FileField нужно уточнить тип
    creator_id: Optional[int] = None
    updator_id: Optional[int] = None


class BranchSchemaCreate(BranchSchemaBase):
    pass


class BranchSchemaUpdate(BaseModel):
    title: Optional[str] = None
    branch_id: Optional[int] = None
    organization_id: Optional[int] = None
    content: Optional[Any] = None
    updator_id: Optional[int] = None


class BranchSchema(BranchSchemaBase):
    id: int
    created_at: datetime.datetime
    update_at: datetime.datetime

    class Config:
        from_attributes = True  # Ранее называлось orm_mode=True в Pydantic v1
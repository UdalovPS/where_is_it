"""storage/database/db/postgres_alchemy/models/spots
Данные по странам
"""
from typing import Union, Optional
import uuid
import logging

from sqlalchemy import text, ForeignKey, select, update, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from datetime import datetime, timezone


from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class SpotsTable(Base):
    __tablename__ = "spots_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shelf_id: Mapped[int] = mapped_column(ForeignKey("shelves_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items_table.id", ondelete="CASCADE"))
    cell_number: Mapped[int] = mapped_column(nullable=False)
    floor_number: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class SpotsDAL(database.BaseBranchSchemas):
    pass
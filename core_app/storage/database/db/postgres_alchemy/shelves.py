"""storage/database/db/postgres_alchemy/models/shelves
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


class ShelvesTable(Base):
    __tablename__ = "shelves_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"), nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    x1: Mapped[int] = mapped_column(nullable=False)
    y1: Mapped[int] = mapped_column(nullable=False)
    x2: Mapped[int] = mapped_column(nullable=False)
    y2: Mapped[int] = mapped_column(nullable=False)
    cell_count: Mapped[int] = mapped_column(nullable=False)
    floor_count: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class ShelvesDAL(database.BaseBranchSchemas):
    pass
"""storage/database/db/postgres_alchemy/models/client_location
Данные по странам
"""
from typing import Union
import uuid

from sqlalchemy import text, ForeignKey, select, update, JSON, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class ClientLocationTable(Base):
    __tablename__ = "client_location_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients_table.id", ondelete="CASCADE"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

class ClientLocationDAL(database.BaseBranches):
    pass
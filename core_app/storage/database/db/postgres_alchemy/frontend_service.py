"""storage/database/db/postgres_alchemy/models/messengers
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


class FrontendServicesTable(Base):
    __tablename__ = "frontend_services_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[int] = mapped_column(default=1)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="SET NULL"), nullable=True)


class MessengersDAL(database.BaseBranches):
    pass
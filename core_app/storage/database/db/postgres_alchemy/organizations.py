"""storage/database/db/postgres_alchemy/models/customer
"""
import logging
from datetime import datetime

from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import logging

from .alchemy_core import Base
from storage.base_interfaces import database


logger = logging.getLogger(__name__)


class OrganizationsTable(Base):
    __tablename__ = "organizations_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40))
    detail: Mapped[str] = mapped_column(nullable=False)
    access_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class CustomersDAL(database.BaseOrganizations):
    pass
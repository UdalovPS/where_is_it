"""database/organizations"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_core import Base


if TYPE_CHECKING:
    from database.users.model import UsersTable


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

    creator = relationship("UsersTable", foreign_keys=[creator_id])
    updator = relationship("UsersTable", foreign_keys=[updator_id])
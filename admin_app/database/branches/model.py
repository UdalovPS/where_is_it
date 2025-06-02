"""database/branches"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base

if TYPE_CHECKING:
    from database.users.model import UsersTable
    from database.organizations.model import OrganizationsTable
    from database.cities.model import CitiesTable


class BranchesTable(Base):
    __tablename__ = "branches_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

    city = relationship("CitiesTable")
    organization = relationship("OrganizationsTable")
    creator = relationship("UsersTable", foreign_keys=[creator_id])
    updator = relationship("UsersTable", foreign_keys=[updator_id])
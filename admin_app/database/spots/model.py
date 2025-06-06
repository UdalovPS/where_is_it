"""database/spots"""

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import text, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_core import Base

if TYPE_CHECKING:
    from database.organizations.model import OrganizationsTable
    from database.shelves.model import ShelvesTable
    from database.users.model import UsersTable
    from database.items.model import ItemsTable


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

    organization = relationship("OrganizationsTable")
    shelf = relationship("ShelvesTable")
    item = relationship("ItemsTable")
    creator = relationship("UsersTable", foreign_keys=[creator_id])
    updator = relationship("UsersTable", foreign_keys=[updator_id])

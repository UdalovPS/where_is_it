"""database/shelves"""

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import text, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_core import Base

if TYPE_CHECKING:
    from database.organizations.model import OrganizationsTable
    from database.branches.model import BranchesTable


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

    organization = relationship("OrganizationsTable")
    branch = relationship("BranchesTable")
    creator = relationship("UsersTable", foreign_keys=[creator_id])
    updator = relationship("UsersTable", foreign_keys=[updator_id])

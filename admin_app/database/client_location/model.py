"""database/client_location"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import text, ForeignKey, Column, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base

if TYPE_CHECKING:
    from database.clients.model import ClientsTable
    from database.branches.model import BranchesTable


class ClientLocationTable(Base):
    __tablename__ = "client_location_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients_table.id", ondelete="CASCADE"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

    client = relationship("ClientsTable")
    branch = relationship("BranchesTable")
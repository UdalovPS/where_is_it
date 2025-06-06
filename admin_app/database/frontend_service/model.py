"""database/frontend_service"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base

if TYPE_CHECKING:
    from database.organizations.model import OrganizationsTable


class FrontendServicesTable(Base):
    __tablename__ = "frontend_services_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[int] = mapped_column(default=1)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="SET NULL"), nullable=True)

    organization = relationship("OrganizationsTable")
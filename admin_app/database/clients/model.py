"""database/clients"""

from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey, Column, JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base

if TYPE_CHECKING:
    from database.frontend_service.model import FrontendServicesTable


class ClientsTable(Base):
    __tablename__ = "clients_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    frontend_service_id: Mapped[int] = mapped_column(ForeignKey("frontend_services_table.id", ondelete='CASCADE'))
    frontend_id = Column(BigInteger)
    frontend_data = Column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

    frontend = relationship("FrontendServicesTable")
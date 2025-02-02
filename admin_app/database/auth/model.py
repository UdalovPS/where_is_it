"""database/auth"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base

if TYPE_CHECKING:
    from database.customer.model import CustomersTable


class AuthTokenTable(Base):
    """Таблица в которой содержатся данные о токенах доступа для API
    Attr:
        id: идентификатор записи
        token: значение токена доступа (именно это значение будет прилетать в запросе)
        name: название токена (для удобства опозначания)
        customer_id: уровень доступа который дан данному токену (чем ниже, тем больше доступно)
        details: опциональное описание токена
        created_at: дата создания
        update_at: дата обновления
    """
    __tablename__ = "auth_token_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True, default=uuid.uuid1)
    name: Mapped[str] = mapped_column(nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers_table.id"))
    details: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    update_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )
    customer: Mapped["CustomersTable"] = relationship("CustomersTable")

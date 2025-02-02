"""database/customer"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_core import Base


if TYPE_CHECKING:
    from database.auth.model import AuthTokenTable


class CustomersTable(Base):
    """ Таблица для всех заказчиков независимо от мессенджера
    Attr:
        id: уникальный идентификатор заказчика
        name: имя заказчика (опционально)
        phone: номер телефона заказчика
        email: почта заказчика
        login: логин для получения счета по токенам
        password: пароль для получения счета по токенам
    """
    __tablename__ = "customers_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40))
    phone: Mapped[str] = mapped_column(String(12), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    login: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    access_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
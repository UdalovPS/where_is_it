"""storage/database/db/postgres_alchemy/models/customer
Данные по аутентификации
"""
import logging
from datetime import datetime

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column
import logging

from .alchemy_core import Base
from storage.base_interfaces import database


logger = logging.getLogger(__name__)


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


class CustomersDAL(database.BaseCustomer):
    pass
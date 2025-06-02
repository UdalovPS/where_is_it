"""database/users"""

from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.db_core import Base


class UsersTable(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[int] = mapped_column(nullable=False, default=2)
    phone: Mapped[str] = mapped_column(String(18), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    login: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    blocked: Mapped[bool] = mapped_column(default=False)
    verify: Mapped[bool] = mapped_column(default=False)
"""storage/database/db/postgres_alchemy/models/auth
Данные по аутентификации
"""
from typing import Union
import uuid
import secrets

from sqlalchemy import text, ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class AuthTokenTable(Base):
    __tablename__ = "auth_token_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True, default=uuid.uuid1)
    name: Mapped[str] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"), nullable=True)
    details: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    update_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow()
    )


class AuthTokenDAL(database.BaseAuth):
    """Класс для взаимодействия с данными об аутентификации в БД"""

    async def get_data_by_token(self, token: str)-> Union[storage_schem.AuthSchem, None]:
        """Метод извлекает данные по токену
        Args:
            token: токен авторизации закрепленный за заказчиком
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = select(AuthTokenTable).where(AuthTokenTable.token == token)
                    res = await session.execute(query)
                    data = res.fetchone()
                    if data is not None:
                        auth_data = storage_schem.AuthSchem.model_validate(
                            from_attributes=True,
                            obj=data[0]
                        )
                        return auth_data

        except Exception as _ex:
            logger.warning(f"Ошибка при извлечении данных по токену: {token} -> {_ex}")

    async def update_token(self, node_id: int) -> Union[str, None]:
        """Метод обновляет токен по идентификатору записи
        Args:
            node_id: идентификатор записи в БД аутентификации
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    new_token = str(secrets.token_hex(64))
                    query = update(AuthTokenTable).where(
                        AuthTokenTable.id == node_id
                    ).values(token=new_token)
                    res = await session.execute(query)
                    await session.commit()
                    if res.rowcount > 0:  # если изменения в БД прошли успешно
                        logger.info(f"Токен для записи №{node_id} успешно изменен")
                        return new_token
        except Exception as _ex:
            logger.warning(f"Ошибка при изменении токена записи №{node_id} -> {_ex}")

    async def add_new_token(self, customer_id: int, name: str)-> Union[storage_schem.AuthSchem, None]:
        """Метод создающий новый токен и закрепляющий его за заказчиком
        Args:
            customer_id: идентификатор заказчика
            name: название токена (для визуализации и читаемости кода)
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    new_record = AuthTokenTable(
                        token=str(secrets.token_hex(64)),
                        name=name,
                        customer_id=customer_id
                    )
                    session.add(new_record)
                    await session.flush()
                    return storage_schem.AuthSchem.model_validate(
                        from_attributes=True,
                        obj=new_record,
                    )
        except Exception as _ex:
            logging.warning(f"Ошибка при добавлении нового токена для заказчика: {customer_id} -> {_ex}")



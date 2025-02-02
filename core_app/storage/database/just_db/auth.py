"""storage/database/just_db/auth"""
from typing import Union

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class AuthJustDb(database.BaseAuth):
    """Данный объект отвечает за взаимодействие с БД
    касающимися для получения данных аутентификации
    """
    db = db_choicer.choice_db_auth_obj(db_type=config.DB_TYPE)

    async def get_data_by_token(self, token: str) -> Union[storage_schem.AuthSchem, None]:
        """Метод извлекает данные по токену
        Args:
            token: токен авторизации закрепленный за заказчиком
        """
        return await self.db.get_data_by_token(token=token)

    async def update_token(self, node_id: int) -> Union[str, None]:
        """Метод обновляет токен по идентификатору записи
        Args:
            node_id: идентификатор записи в БД аутентификации
        """
        return await self.db.update_token(node_id=node_id)

    async def add_new_token(self, customer_id: int, name: str)\
            -> Union[storage_schem.AuthSchem, None]:
        """Метод создающий новый токен и закрепляющий его за заказчиком
        Args:
            customer_id: идентификатор заказчика
            name: название токена (для визуализации и читаемости кода)
        """
        return await self.db.add_new_token(customer_id=customer_id, name=name)


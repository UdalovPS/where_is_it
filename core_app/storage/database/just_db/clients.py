"""storage/database/just_db/clients"""
from typing import Union

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class ClientsJustDb(database.BaseClient):
    """Данный объект отвечает за взаимодействие с БД
    касающимися для получения данных клиента
    """
    db = db_choicer.choice_db_client_obj(db_type=config.DB_TYPE)

    async def add_new_client(
            self,
            messenger_id: int,
            messenger_type: int,
            name: Union[str, None],
            phone: Union[str, None],
            username: Union[str, None],
            age: Union[int, None]
    ) -> storage_schem.ClientSchem:
        """Данный метод добавляет нового клиента в БД
         Args:
             messenger_id: идентификатор из мессенджера/приложения
             messenger_type: тип мессенджера/приложения
             name: имя клиента (не обязательный параметр)
             phone: номер телефона клиента (не обязательный параметр)
             username: username клиента (не обязательный параметр)
             age: возраст клиента (не обязательный параметр)
        """
        return await self.db.add_new_client(
            messenger_id=messenger_id,
            messenger_type=messenger_type,
            name=name,
            phone=phone,
            username=username,
            age=age
        )

    async def get_client_data_by_messenger_id(
            self,
            messenger_id: int,
            messenger_type: int
    ) -> Union[storage_schem.ClientSchem, None]:
        """Метод извлекающий данные клиента из БД
        Args:
            messenger_id: идентификатор из мессенджера/приложения
            messenger_type: тип мессенджера/приложения
        """
        return await self.db.get_client_data_by_messenger_id(
            messenger_id=messenger_id,
            messenger_type=messenger_type
        )

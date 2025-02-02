from typing import Union, Any

from storage.base_interfaces import database
from schemas import storage_schem


class ClientTest(database.BaseClient):
    """Метод для тестового взаимодействия с БД при разработке
    приложения. Отвечает за хранение данных клиента
    """
    clients_data = {
        1: {
            "messenger_id": 1,
            "messenger_type": 1,
            "name": "test_client_1",
            "phone": "test_client_1_phone",
            "username": "test_client_1_username",
            "age": 11
        },
        2: {
            "messenger_id": 2,
            "messenger_type": 1,
            "name": "test_client_2",
            "phone": "test_client_2_phone",
            "username": "test_client_2_username",
            "age": 22
        },
    }

    async def add_new_client(
            self,
            messenger_id: int,
            messenger_type: int,
            name: Union[str, None] = None,
            phone: Union[str, None] = None,
            username: Union[str, None] = None,
            age: Union[int, None] = None
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
        self.clients_data[3] = {
            "messenger_id": 1,
            "messenger_type": 1,
            "name": "test_client_3",
            "phone": "test_client_3_phone",
            "username": "test_client_3_username",
            "age": 33
        }
        return storage_schem.ClientSchem(
            id=3,
            messenger_id=self.clients_data[3]["messenger_id"],
            messenger_type=self.clients_data[3]["messenger_type"],
            name=self.clients_data[3]["name"],
            phone=self.clients_data[3]["phone"],
            username=self.clients_data[3]["username"],
            age=self.clients_data[3]["age"]
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
        for key, value in self.clients_data.items():
            if value["messenger_id"] == messenger_id and value["messenger_type"] == messenger_type:
                return storage_schem.ClientSchem(
                    id=key,
                    messenger_id=self.clients_data[key]["messenger_id"],
                    messenger_type=self.clients_data[key]["messenger_type"],
                    name=self.clients_data[key]["name"],
                    phone=self.clients_data[key]["phone"],
                    username=self.clients_data[key]["username"],
                    age=self.clients_data[key]["age"]
                )


if __name__ == '__main__':
    import asyncio
    obj = ClientTest()
    print(asyncio.run(obj.add_new_client(1, 1)))
    print(asyncio.run(obj.get_client_data_by_messenger_id(2, 1)))

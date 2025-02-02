from storage.base_interfaces import database
from . import just_db

def choice_customer_obj(storage_type: str) -> database.BaseCustomer:
    """Данный метод исходя из глобальных настроек выбирает объект
    для взаимодействия с данными заказчика
    Args:
        storage_type: ключ по которому извлекаются данные по паттерну стратегия
    """
    data_dict = {
        "just_db": just_db.CustomerJustDb
    }
    return data_dict[storage_type]()


def choice_client_obj(storage_type: str) -> database.BaseClient:
    """Данный метод исходя из глобальных настроек выбирает объект
    для взаимодействия с клиентскими данными
    Args:
        storage_type: ключ по которому извлекаются данные по паттерну стратегия
    """
    data_dict = {
        "just_db": just_db.ClientsJustDb
    }
    return data_dict[storage_type]()


def choice_auth_obj(storage_type: str) -> database.BaseAuth:
    """Данный метод исходя из глобальных настроек выбирает объект
    для взаимодействия с данными аутентификации
    Args:
        storage_type: ключ по которому извлекаются данные по паттерну стратегия
    """
    data_dict = {
        "just_db": just_db.AuthJustDb
    }
    return data_dict[storage_type]()

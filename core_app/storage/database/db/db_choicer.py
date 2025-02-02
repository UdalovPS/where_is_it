
from storage.base_interfaces import database
from . import db_test
from . import postgres_alchemy


def choice_db_customer_obj(db_type: str) -> database.BaseCustomer:
    """Данный метод возвращает объект для взаимодействия с
    данными заказчика по конфигурационным данным типа БД
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "postgres_alchemy": postgres_alchemy.CustomersDAL
    }
    return choice_db_dict[db_type]()

def choice_db_client_obj(db_type: str) -> database.BaseClient:
    """Данный метод возвращает объект для взаимодействия с
    данными клиента по конфигурационным данным типа БД
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": db_test.ClientTest  # !!! исправить
    }
    return choice_db_dict[db_type]()


def choice_db_auth_obj(db_type: str) -> database.BaseAuth:
    """Данный метод возвращает объект для взаимодействия с
    данными аутентификации по конфигурационным данным типа БД
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.AuthTokenDAL
    }
    return choice_db_dict[db_type]()

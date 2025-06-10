
from storage.base_interfaces import database
from . import db_test
from . import postgres_alchemy


def choice_db_customer_obj(db_type: str) -> database.BaseOrganizations:
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
        "postgres_alchemy": postgres_alchemy.ClientsDAL
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


def choice_branch_schemas_obj(db_type: str) -> database.BaseBranchSchemas:
    """Данный метод возвращает объект для взаимодействия с
    данными схем филиалов (работа с файлами)
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.BranchSchemasDAL
    }
    return choice_db_dict[db_type]()

def choice_items_obj(db_type: str) -> database.BaseItems:
    """Данный метод возвращает объект для взаимодействия с
    данными товаров разложенных на полках
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.ItemsDAL
    }
    return choice_db_dict[db_type]()

def choice_spots_obj(db_type: str) -> database.BaseSpot:
    """Данный метод возвращает объект для взаимодействия с
    данными ячеек на которых разложены товары
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.SpotsDAL
    }
    return choice_db_dict[db_type]()

def choice_branches_obj(db_type: str) -> database.BaseBranches:
    """Данный метод возвращает объект для взаимодействия с
    данными филиалов
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.BranchesDAL
    }
    return choice_db_dict[db_type]()

def choice_client_location_obj(db_type: str) -> database.BaseClientLocation:
    """Данный метод возвращает объект для взаимодействия с
    локацией клиента
    Args:
        db_type: тип базы данных
    """
    choice_db_dict = {
        "db_test": db_test.ClientTest,
        "postgres_alchemy": postgres_alchemy.ClientLocationDAL
    }
    return choice_db_dict[db_type]()
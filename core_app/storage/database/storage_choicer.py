from storage.base_interfaces import database
from . import just_db


def choice_customer_obj(storage_type: str) -> database.BaseOrganizations:
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

def choice_branch_schemas_obj(storage_type: str) -> database.BaseBranchSchemas:
    """Данный метод исходя из глобальных настроек выбирает объект
    для взаимодействия с данными схем филиалов (работа с файлами)
    Args:
        storage_type: ключ по которому извлекаются данные по паттерну стратегия
    """
    data_dict = {
        "just_db": just_db.BranchSchemasJustDb
    }
    return data_dict[storage_type]()

def choice_items_obj(storage_type: str) -> database.BaseItems:
    data_dict = {
        "just_db": just_db.ItemsJustDb
    }
    return data_dict[storage_type]()

def choice_spots_obj(storage_type: str) -> database.BaseSpot:
    data_dict = {
        "just_db": just_db.SpotsJustDb
    }
    return data_dict[storage_type]()

def choice_branches_obj(storage_type: str) -> database.BaseBranches:
    data_dict = {
        "just_db": just_db.BranchesJustDb
    }
    return data_dict[storage_type]()

def choice_client_location_obj(storage_type: str) -> database.BaseClientLocation:
    data_dict = {
        "just_db": just_db.ClientLocationJustDb
    }
    return data_dict[storage_type]()

def choice_countries_obj(storage_type: str) -> database.BaseCountry:
    data_dict = {
        "just_db": just_db.CountriesJustDb
    }
    return data_dict[storage_type]()

def choice_district_obj(storage_type: str) -> database.BaseDistrict:
    data_dict = {
        "just_db": just_db.DistrictsJustDb
    }
    return data_dict[storage_type]()

def choice_cities_obj(storage_type: str) -> database.BaseCity:
    data_dict = {
        "just_db": just_db.CitiesJustDb
    }
    return data_dict[storage_type]()

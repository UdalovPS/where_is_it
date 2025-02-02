"""storage/database/just_db/customer"""
from typing import Union

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class CustomerJustDb(database.BaseCustomer):
    """Данный объект отвечает за взаимодействие с БД
    касающимися для получения данных заказчика
    """
    db = db_choicer.choice_db_customer_obj(db_type=config.DB_TYPE)
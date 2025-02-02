from typing import Union

from pydantic import BaseModel


class ClientSchem(BaseModel):
    """Схема для представления данных клиента"""
    id: int
    messenger_id: int
    messenger_type: int
    name: Union[str, None]
    phone: Union[str, None]
    username: Union[str, None]
    age: Union[int, None]

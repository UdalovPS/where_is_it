"""Модуль с ошибками"""

from schemas import base_schemas

class AuthenticationError(Exception):
    """Ошибка авторизации запроса"""
    def __init__(self, token: str, api: str):
        self.token = token
        self.error = base_schemas.BaseErrorSchem(
            name="AuthenticationError",
            details="Invalid access token",
            api=api,
            status_code=401
        )

    def __str__(self):
        return f"Send not valid token -> {self.token}"


class AccessError(Exception):
    """Ошибка когда у пользователя нет доступа к запрашиваемому ресурсу"""
    def __init__(self, api: str):
        self.api = api
        self.error = base_schemas.BaseErrorSchem(
            name="AccessError",
            details="no access to this resource",
            api=api,
            status_code=403
        )

    def __str__(self):
        return f"AccessError api -> {self.api}"


class NotFoundError(Exception):
    """Ошибка когда не удалось найти какие-то значения"""
    def __init__(self, item_name: str, api: str):
        self.item_name = item_name
        self.error = base_schemas.BaseErrorSchem(
            name="NotFoundError",
            details=f"not found item: <{item_name}>",
            api=api,
            status_code=200
        )

    def __str__(self):
        return f"NotFoundError item_name -> {self.item_name}"


class ValidationError(Exception):
    """Ошибка когда не прошла первоначальная валидация"""
    def __init__(self, detail: str, api: str):
        self.detail = detail
        self.error = base_schemas.BaseErrorSchem(
            name="DownloadKeyError",
            details=detail,
            api=api,
            status_code=200
        )

    def __str__(self):
        return f"ValidationError -> {self.detail}"


class DownloadKeyError(Exception):
    """Ошибка когда не корректный ключ для скачивания данных изображения"""
    def __init__(self, key: str, api: str):
        self.key = key
        self.error = base_schemas.BaseErrorSchem(
            name="DownloadKeyError",
            details=f"not valid download key: <{key}>",
            api=api,
            status_code=200
        )

    def __str__(self):
        return f"DownloadKeyError key-> {self.key}"


class UpdateLocationError(Exception):
    """Ошибка когда не удалось обновить локацию клиента"""
    def __init__(self, api: str):
        self.error = base_schemas.BaseErrorSchem(
            name="UpdateLocationError",
            details=f"error to add location",
            api=api,
            status_code=400
        )

    def __str__(self):
        return f"UpdateLocationError"


class AddError(Exception):
    """Ошибка при добавлении данных"""
    def __init__(self, api: str, item: str):
        self.item = item
        self.error = base_schemas.BaseErrorSchem(
            name="AddError",
            details=f"error to add data: <{item}>",
            api=api,
            status_code=400
        )

    def __str__(self):
        return f"error to add item data"


class UnknownError(Exception):
    """Неожидаемая ошибка, которую не смогли обработать"""
    def __init__(self, api: str):
        self.error = base_schemas.BaseErrorSchem(
            name="UnknownError",
            details=f"unknown error",
            api=api,
            status_code=500
        )

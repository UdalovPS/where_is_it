import logging
import re
from typing import Union

from sqlalchemy.exc import IntegrityError


from schemas.base_schemas import BaseResultSchem, BaseErrorSchem
import exceptions

logger = logging.getLogger(__name__)


def handle_view_exception(ex: Exception, api: str) -> BaseResultSchem:
    """Метод обработки исключений возникших во view
    Args:
        ex: возникшая ошибка
        api: раздел API в котором возникала ошибка
    """
    if isinstance(ex, exceptions.AccessError):
        logger.error(f"Возникла ошибка допуска. API: {api} ")

    elif isinstance(ex, exceptions.ValidationError):
        logger.error(f"Ошибка валидации данных. detail: {ex.detail}, API: {api}")

    elif isinstance(ex, exceptions.DownloadKeyError):
        logger.error(f"Ошибка загрузки схемы")

    elif isinstance(ex, exceptions.UpdateLocationError):
        logger.error(f"Ошибка при обновлении локации клиента")

    elif isinstance(ex, exceptions.AddError):
        logger.error(f"Ошибка при добавлении данных, API: {api}")

    elif isinstance(ex, exceptions.AuthenticationError):
        logger.error(f"Возникла ошибка аутентификации. token: {ex.token} API: {api}")

    elif isinstance(ex, exceptions.NotFoundError):
        logger.error(f"Возникла ошибка поиска поля {ex.error}, API: {api}")
    else:
        logger.error(f"Возникла неопределенная ошибка -> {ex}, API: {api}")
        ex.error = BaseErrorSchem(
            name="UnknownError",
            details=f"unknown error",
            api=api,
            status_code=500
        )

    return BaseResultSchem(success=False, error=ex.error)



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

    if isinstance(ex, exceptions.AuthenticationError):
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



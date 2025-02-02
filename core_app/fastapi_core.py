"""fastApi core"""

from typing import Union

from fastapi import Header


async def get_token(token: str = Header(alias="auth-token", default=None)) -> Union[str, None]:
    """Данный метод извлекает токен из заголовка приходящего запроса
    Args:
        token: токен, который пришел в заголовке запроса
    """
    return token


from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


# Создаем типовой параметр для Pydantic модели
T = TypeVar("T", bound=BaseModel)


class BaseErrorSchem(BaseModel):
    """Базовая схема по формату которой будут указаны все ошибки
    Attr:
        name: наименование ошибки
        details: подробное описание ошибки
        api: наименование раздела в котором осуществлена ошибка
        status_code: статус код ошибки (для REST интерфейса)
    """
    name: str
    details: Optional[str] = None
    api: str
    status_code: int = 400


class BaseResultSchem(BaseModel, Generic[T]):
    """Базовая схема ответа логических методов
    Attr:
        error: ошибка в ответе, если она есть
        data: данные которые возвращает метод
    """
    error: Optional[BaseErrorSchem] = None
    data: Optional[T] = None


class NullSchem(BaseModel):
    data: str


if __name__ == '__main__':
    class NullSchem(BaseResultSchem):
        data: str

    obj = BaseErrorSchem(name="name", api="api")
    obj2 = NullSchem(error=obj, data="sdas")
    print(obj2)
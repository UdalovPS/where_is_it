from typing import Generic, Optional, TypeVar
import datetime

from pydantic import BaseModel


# Создаем типовой параметр для Pydantic модели
T = TypeVar("T", bound=BaseModel)


def convert_datetimes(obj):
    """
    Рекурсивно преобразует объекты datetime в ISO-строки.
    Если встречается вложенная модель (наследник BaseModel), пытаемся вызвать ее метод model_dump.
    """
    from pydantic import BaseModel

    if isinstance(obj, BaseModel):
        # Если у вложенной модели есть переопределенный model_dump, используем его
        if hasattr(obj, "model_dump"):
            return convert_datetimes(obj.model_dump())
        else:
            return convert_datetimes(obj.dict())
    elif isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(item) for item in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


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
    success: bool = True
    error: Optional[BaseErrorSchem] = None
    data: Optional[T] = None

    def model_dump(self, *args, **kwargs) -> dict:
        # Получаем «сырые» данные модели
        raw_data = super().model_dump(*args, **kwargs)
        # Преобразуем datetime в ISO-строки
        return convert_datetimes(raw_data)


class NullSchem(BaseModel):
    data: str


if __name__ == '__main__':
    class NullSchem(BaseResultSchem):
        data: str

    obj = BaseErrorSchem(name="name", api="api")
    obj2 = NullSchem(error=obj, data="sdas")
    print(obj2)
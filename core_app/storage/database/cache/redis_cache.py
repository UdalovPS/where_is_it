"""Данный модуль отвечает за взаимодействие с Redis"""
import asyncio
from typing import Type, Union
from redis import asyncio as aioredis
from pydantic import BaseModel
import logging

# импортируем глобальные конфигурации
from config import REDIS_PORT, REDIS_PASSWORD, REDIS_EX

# импортируем интерфейсный класс
from storage.base_interfaces.cache import cache_interface

logger = logging.getLogger(__name__)


class Redis(cache_interface.BaseCache):
    """В данном классе будет инкапсулирована вся логика взаимодействия с redis
    через библиотеку aioredis (нужно асинхронное взаимодействие)
    """
    def __init__(self, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.redis = aioredis.from_url(f"redis://:{password}@localhost:{port}")

    async def get_data_from_cache(self, key: str, data_class: Type[BaseModel]) -> Union[BaseModel, None]:
        """Данный метод извлекает из КЭШа json и преобразует его в pydantic
        объект согласно той схемы которую в него передали
        Args:
            key: ключ по которому необходимо искать объект
            data_class: шаблон pydantic объекта, в который нужно преобразовать полученные данные
        return:
            pydantic объект согласно data_class либо None
        """
        try:
            logger.debug(f"Извлекаю данные из КЭШа по ключу: {key}")
            json_data = await self.redis.get(key)
            if json_data:
                return data_class.model_validate_json(json_data)
            logger.debug(f"Данные в КЭШе по ключу: {key} не найдены")
        except Exception as _ex:
            logger.warning(f"Ошибка извлечения pydantic по ключу: {key} из redis => {_ex}")
            return None

    async def set_data_in_cache(self, key: str, value: BaseModel, live_time: int = REDIS_EX) -> bool:
        """Данный метод заносит в КЭШ Pydantic объект
        Args:
            key: ключ по которому заносится объект
            value: значение которое будет спрятано под ключем
            live_time: время в секундах сколько хранится значение в КЭШе
        """
        try:
            logger.debug(f"Сохраняю pudantic объект в КЭШ по ключу: {key} на {live_time} секунд")
            await self.redis.set(key, value.model_dump_json(), ex=live_time)
            return True
        except Exception as _ex:
            logger.warning(f"Ошибка занесения pydantic объекта по ключу {key} => {_ex}")
            return False


if __name__ == '__main__':
    from pydantic import BaseModel

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")

    class TestObj(BaseModel):
        data_1: str
        data_2: str

    obj = TestObj(data_1="data_1", data_2="data_2")
    redis = Redis()

    async def main():
        # set_data = await redis.set_data_in_cache(key='key', value=obj)
        # print(set_data)
        # await asyncio.sleep(2)
        await redis.get_data_from_cache(key="key", data_class=TestObj)

    asyncio.run(main())

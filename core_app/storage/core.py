import logging

import config
from .database import storage_choicer

logger = logging.getLogger(__name__)


class StorageCommon:
    """Класс отвечающий за обобщенное взаимодействие
    с хранилищем данных"""
    customer_obj = storage_choicer.choice_customer_obj(storage_type=config.STORAGE_TYPE)
    client_obj = storage_choicer.choice_client_obj(storage_type=config.STORAGE_TYPE)
    auth_obj = storage_choicer.choice_auth_obj(storage_type=config.STORAGE_TYPE)


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")
    obj = StorageCommon()
    async def main():
        await obj.auth_obj.add_new_token(customer_id=1, name="Мини токен")
        token = await obj.auth_obj.get_data_by_token(token="6748b8ce-d0fc-11ef-b22c-9408535897fd")

    asyncio.run(main())

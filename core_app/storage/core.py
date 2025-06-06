import logging

import config
from storage.database import storage_choicer

logger = logging.getLogger(__name__)


class StorageCommon:
    """Класс отвечающий за обобщенное взаимодействие
    с хранилищем данных"""
    customer_obj = storage_choicer.choice_customer_obj(storage_type=config.STORAGE_TYPE)
    client_obj = storage_choicer.choice_client_obj(storage_type=config.STORAGE_TYPE)
    auth_obj = storage_choicer.choice_auth_obj(storage_type=config.STORAGE_TYPE)
    branch_schemas_obj = storage_choicer.choice_branch_schemas_obj(storage_type=config.STORAGE_TYPE)


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")
    obj = StorageCommon()
    async def main():
        data = await obj.client_obj.get_data_by_messenger_id(messenger_id=1, messenger_type=1)
        print(data)

    asyncio.run(main())

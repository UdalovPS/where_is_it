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
    items_obj = storage_choicer.choice_items_obj(storage_type=config.STORAGE_TYPE)
    spots_obj = storage_choicer.choice_spots_obj(storage_type=config.STORAGE_TYPE)

if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")
    obj = StorageCommon()
    async def main():
        data = await obj.branch_schemas_obj.get_data_by_branch_id(branch_id=1)
        print(data)

    asyncio.run(main())

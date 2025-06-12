import logging

import config
from storage.database import storage_choicer
from storage.database.cache.cache_choicer import get_cache_obj

logger = logging.getLogger(__name__)


class StorageCommon:
    """Класс отвечающий за обобщенное взаимодействие
    с хранилищем данных"""
    cache_obj = get_cache_obj(key=config.CACHE_TYPE)    # объект для взаимодействия с КЭШем

    customer_obj = storage_choicer.choice_customer_obj(storage_type=config.STORAGE_TYPE)
    client_obj = storage_choicer.choice_client_obj(storage_type=config.STORAGE_TYPE)
    auth_obj = storage_choicer.choice_auth_obj(storage_type=config.STORAGE_TYPE)
    branch_schemas_obj = storage_choicer.choice_branch_schemas_obj(storage_type=config.STORAGE_TYPE)
    items_obj = storage_choicer.choice_items_obj(storage_type=config.STORAGE_TYPE)
    spots_obj = storage_choicer.choice_spots_obj(storage_type=config.STORAGE_TYPE)
    branches_obj = storage_choicer.choice_branches_obj(storage_type=config.STORAGE_TYPE)
    client_location_obj = storage_choicer.choice_client_location_obj(storage_type=config.STORAGE_TYPE)
    countries_obj = storage_choicer.choice_countries_obj(storage_type=config.STORAGE_TYPE)
    district_obj = storage_choicer.choice_district_obj(storage_type=config.STORAGE_TYPE)
    cities_obj = storage_choicer.choice_cities_obj(storage_type=config.STORAGE_TYPE)

if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s")
    obj = StorageCommon()
    async def main():
        # data = await obj.branches_obj.get_data_by_geo(organization_id=1, latitude=58.022030, longitude=56.271377, limit=3)
        data = await obj.client_obj.get_data_by_frontend_id(
            frontend_id=1, frontend_service_id=1, organization_id=1
        )
        print(data)
        data = await obj.client_obj.add_new_client(
            name="tesst",
            frontend_service_id=1,
            frontend_id=1,
            frontend_data={1: 1}
        )
        # print(data)
        print(data)

    asyncio.run(main())

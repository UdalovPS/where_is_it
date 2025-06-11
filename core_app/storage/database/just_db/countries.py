"""storage/database/just_db/countries"""
from typing import Optional, List

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class CountriesJustDb(database.BaseCountry):
    """Данный объект отвечает за взаимодействие с БД
    касающимися стран
    """
    db = db_choicer.choice_countries_obj(db_type=config.DB_TYPE)

    async def get_countries_by_org(self, organization_id: int) -> Optional[
        List[storage_schem.countries_schem.CountrySchem]]:
        """Извлекаем список стран одной организации
        Args:
              organization_id: идентификатор организации
        """
        return await self.db.get_countries_by_org(organization_id=organization_id)
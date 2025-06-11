"""storage/database/just_db/cities"""
from typing import Optional, List

from schemas import storage_schem
from storage.base_interfaces import database
from ..db import db_choicer

import config


class CitiesJustDb(database.BaseCity):
    """Данный объект отвечает за взаимодействие с БД
    касающимися регионов
    """
    db = db_choicer.choice_cities_obj(db_type=config.DB_TYPE)

    async def get_similar_by_org_district_and_name(
            self,
            organization_id: int,
            search_name: str,
            district_id: int,
            limit: int = 3,
            similarity_threshold: float = 0.1
    ) -> Optional[List[storage_schem.cities_schem.CitySchem]]:
        """Поиск списка похожих названий населенного пункта
        определенной организации
        Args:
            organization_id: идентификатор организации
            search_name: имя похожее на которое нужно найти
            district_id: идентификатор региона
            limit: кол-во извлекаемых записей
            similarity_threshold: доля похожести после которой запись входит в поле зрения
        """
        return await self.db.get_similar_by_org_district_and_name(
            organization_id=organization_id,
            search_name=search_name,
            limit=limit,
            similarity_threshold=similarity_threshold,
            district_id=district_id
        )
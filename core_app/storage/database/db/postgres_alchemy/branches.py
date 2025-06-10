"""storage/database/db/postgres_alchemy/models/branches
Данные по странам
"""
from typing import Optional, List

from sqlalchemy import text, ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
import logging

from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class BranchesTable(Base):
    __tablename__ = "branches_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class BranchesDAL(database.BaseBranches):
    async def get_data_by_geo(
            self,
            organization_id: int,
            latitude: float,
            longitude: float,
            limit: int
    ) -> Optional[List[storage_schem.branches_schem.BranchSchema]]:
        """Извлечение ближайших к текущей геолокации филиалов
        Args:
            organization_id: идентификатор организации
            latitude: широта, от которой требуется вести поиск
            longitude: долгота от который требуется вести поиск
            limit: кол-во записей, которые нужно вернуть
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT
                            br.id AS branch_id,
                            br.name AS branch_name,
                            address,
                            br.organization_id,
                            latitude,
                            longitude,
                            SQRT(POWER(latitude - :latitude, 2) + POWER(longitude - :longitude, 2)) AS distance,
                            ci.id AS city_id,
                            ci.name AS city_name,
                            di.id AS district_id,
                            di.name AS district_name,
                            co.id AS country_id,
                            co.name AS country_name
                        FROM 
                            branches_table br
                        JOIN 
                            cities_table ci ON ci.id = br.city_id
                        JOIN
                            districts_table di ON di.id = ci.district_id
                        JOIN
                            countries_table co ON co.id = di.country_id
                        WHERE 
                            br.organization_id = :organization_id
                        ORDER BY 
                            distance
                        LIMIT
                            :limit
                    """)

                    result = await session.execute(
                        query,
                        {"latitude": latitude, "longitude": longitude, "organization_id": organization_id, "limit": limit}
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None

                    return [
                        storage_schem.branches_schem.BranchSchema(
                            id=row.branch_id,
                            name=row.branch_name,
                            address=row.address,
                            city_data=storage_schem.cities_schem.CitySchem(
                                id=row.city_id,
                                name=row.city_name,
                                organization_id=row.organization_id,
                                district_data=storage_schem.districts_schem.DistrictSchem(
                                    id=row.district_id,
                                    name=row.district_name,
                                    organization_id=row.organization_id,
                                    country_data=storage_schem.countries_schem.CountrySchem(
                                        id=row.country_id,
                                        name=row.country_name,
                                        organization_id=row.organization_id,
                                    )
                                )
                            ),
                            organization_id=row.organization_id,
                            latitude=row.latitude,
                            longitude=row.longitude,
                        ) for row in rows
                    ]
        except Exception as ex:
            logger.critical(
                f"Ошибка при извлечении ближайших филиалов по геолокации, "
                f"organization_id: {organization_id} latitude: {latitude}, "
                f"longitude: {longitude}, limit: {limit} -> {ex}")
            return None
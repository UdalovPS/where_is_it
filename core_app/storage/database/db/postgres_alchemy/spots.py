"""storage/database/db/postgres_alchemy/models/spots
Данные по странам
"""
from typing import Optional, List
import logging

from sqlalchemy import text, ForeignKey, select, update, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from datetime import datetime, timezone


from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class SpotsTable(Base):
    __tablename__ = "spots_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shelf_id: Mapped[int] = mapped_column(ForeignKey("shelves_table.id", ondelete="CASCADE"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items_table.id", ondelete="CASCADE"))
    cell_number: Mapped[int] = mapped_column(nullable=False)
    floor_number: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class SpotsDAL(database.BaseSpot):
    async def get_data_by_item_and_organization(
            self,
            items_ids: List[int],
            org_id: int,
            branch_id: int
    ) -> Optional[List[storage_schem.spots_schem.SpotsWithShelvesSchem]]:
        """Извлечение данных по товару и организации
        Args:
            items_ids: список идентификаторов товаров которые необходим найти на полках
            org_id: идентификатор организации
            branch_id: идентификатор филиала в котором осуществляется поиск
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT
                            sp.id AS spot_id,
                            sp.shelf_id,
                            sp.organization_id,
                            sp.item_id,
                            sp.cell_number,
                            sp.floor_number,
                            sp.creator_id AS spot_creator_id,
                            sp.updator_id AS spot_updator_id,
                            sp.created_at AS spot_created_at,
                            sp.update_at AS spot_update_at,
                            sh.name,
                            sh.branch_id,
                            sh.x1,
                            sh.y1,
                            sh.x2,
                            sh.y2,
                            sh.cell_count,
                            sh.floor_count,
                            sh.creator_id AS shelf_creator_id,
                            sh.updator_id AS shelf_updator_id,
                            sh.created_at AS shelf_created_at,
                            sh.update_at AS shelf_update_at,
                            it.name AS item_name
                        FROM 
                            spots_table sp
                        JOIN 
                            shelves_table sh ON sp.shelf_id = sh.id
                        JOIN
                            items_table it ON it.id = sp.item_id
                        JOIN
                            branches_table br ON br.id = sh.branch_id
                        WHERE 
                            sp.item_id = ANY(:items_ids)
                            AND sp.organization_id = :organization_id
                            AND br.id = :branch_id
                        ORDER BY 
                            sp.item_id
                    """)

                    result = await session.execute(
                        query,
                        {"items_ids": tuple(items_ids), "organization_id": org_id, "branch_id": branch_id}
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None

                    return [
                        storage_schem.spots_schem.SpotsWithShelvesSchem(
                            id=row.spot_id,
                            organization_id=row.organization_id,
                            cell_number=row.cell_number,
                            floor_number=row.floor_number,
                            creator_id=row.spot_creator_id,
                            updator_id=row.spot_updator_id,
                            created_at=row.spot_created_at,
                            update_at=row.spot_update_at,
                            shelf_data = storage_schem.spots_schem.ShelfSchem(
                                id=row.shelf_id,
                                name=row.name,
                                branch_id=row.branch_id,
                                organization_id=row.organization_id,
                                x1=row.x1,
                                y1=row.y1,
                                x2=row.x2,
                                y2=row.y2,
                                cell_count=row.cell_count,
                                floor_count=row.floor_count,
                                creator_id=row.shelf_creator_id,
                                updator_id=row.shelf_updator_id,
                                created_at=row.shelf_created_at,
                                update_at=row.shelf_update_at
                            ),
                            item_data = storage_schem.spots_schem.ItemDataSchem(
                                id=row.item_id,
                                name=row.item_name
                            )
                        )
                    for row in rows]
        except Exception as ex:
            logger.critical(
                f"Ошибка при извлечении спотов. items_ids: {items_ids}, organization_id: {org_id} -> {ex}")
            return None
"""storage/database/db/postgres_alchemy/models/items
Данные по странам
"""
from abc import ABC
from typing import Optional, List
import uuid
import logging

from sqlalchemy import text, ForeignKey, select, update, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from datetime import datetime, timezone


from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


class ItemsTable(Base):
    __tablename__ = "items_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub_id: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories_table.id", ondelete='CASCADE'))
    details: Mapped[str] = mapped_column(nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class ItemsDAL(database.BaseItems):
    async def get_similar_items(
            self, branch_id: int,
            search_name: str,
            sim_threshold: float = 0.1,
            count: int = 10
    ) -> Optional[List[storage_schem.items.SimilarItemsSchem]]:
        """Извлечение всех похожих по имени товаров лежащих
        на полках в помещении нужного филиала
        Args:
            branch_id: идентификатор филиала
            search_name: наименование по которому ведется поиск товара
            sim_threshold: процент похожести, по которому выдается поиск из БД
            count: кол-во записей которое нужно извлечь из БД
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = text("""
                        SELECT DISTINCT
                            i.id,
                            i.name,
                            similarity(i.name, :search_name) AS similarity_score
                        FROM 
                            items_table i
                        JOIN 
                            spots_table sp ON i.id = sp.item_id
                        JOIN
                            shelves_table s ON sp.shelf_id = s.id
                        JOIN
                            branches_table b ON s.branch_id = b.id
                        WHERE 
                            b.id = :branch_id
                            AND similarity(i.name, :search_name) > :similarity_threshold
                        ORDER BY 
                            similarity_score DESC
                        LIMIT :count
                    """)

                    result = await session.execute(
                        query,
                        {"branch_id": branch_id, "search_name": search_name, "similarity_threshold": sim_threshold, "count": count}
                    )
                    rows = result.fetchall()

                    if not rows:
                        return None
                    # return [dict(row._mapping) for row in rows]
                    return [storage_schem.items.SimilarItemsSchem.model_validate(row) for row in rows]

        except Exception as ex:
            logger.critical(
                f"Ошибка при извлечении всех товаров относящихся к определенному филиалу: {branch_id} -> {ex}")
            return None
"""storage/database/db/postgres_alchemy/models/branch_schemas
Данные по странам
"""
from typing import Union, Optional
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


class BranchSchemasTable(Base):
    __tablename__ = "branch_schemas_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"), nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    content = Column(FileField)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class BranchSchemasDAL(database.BaseBranchSchemas):
    async def get_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchSchema]:
        """Извлечение данных по первичному ключу
        Args:
            node_id: идентификатор записи
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = select(BranchSchemasTable).where(BranchSchemasTable.id == node_id)
                    res = await session.execute(query)
                    data = res.fetchone()
                    if data is not None:
                        res_data = storage_schem.branches_schem.BranchSchema.model_validate(
                            obj=data[0]
                        )
                        return res_data

        except Exception as _ex:
            logger.critical(f"Ошибка при извлечении данных схемы помещения: {node_id} -> {_ex}")
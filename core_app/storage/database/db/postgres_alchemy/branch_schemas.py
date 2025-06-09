"""storage/database/db/postgres_alchemy/models/branch_schemas
Данные по странам
"""
from typing import Optional
import logging
import os
from datetime import datetime
import contextlib

from sqlalchemy import text, ForeignKey, select, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_file import FileField
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.providers import get_driver
from libcloud.storage.types import (
    ContainerAlreadyExistsError,
    Provider,
)


from .alchemy_core import Base, async_session_maker

from storage.base_interfaces import database
from schemas import storage_schem


logger = logging.getLogger(__name__)


# настраиваем хранилище
os.makedirs("/var/wii", 0o777, exist_ok=True)
driver = get_driver(Provider.LOCAL)("/var/wii")

with contextlib.suppress(ContainerAlreadyExistsError):
    driver.create_container(container_name="branch_schemas")
container = driver.get_container(container_name="branch_schemas")
StorageManager.add_storage("branch_schemas", container)


class BranchSchemasTable(Base):
    __tablename__ = "branch_schemas_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"), nullable=True, unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    content = Column(FileField(upload_storage="branch_schemas"))
    exit_x: Mapped[int] = mapped_column(nullable=False)
    exit_y: Mapped[int] = mapped_column(nullable=False)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)


class BranchSchemasDAL(database.BaseBranchSchemas):
    async def get_by_id(self, node_id: int) -> Optional[storage_schem.branches_schem.BranchPlanSchemaBase]:
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
                        res_data = storage_schem.branches_schem.BranchPlanSchemaBase.model_validate(obj=data[0])
                        return res_data

        except Exception as _ex:
            logger.critical(f"Ошибка при извлечении данных схемы помещения: {node_id} -> {_ex}")

    async def get_data_by_branch_id(self, branch_id: int) -> Optional[storage_schem.branches_schem.BranchPlanSchemaBase]:
        """Извлечение данных по ID филиала
        Args:
            branch_id: идентификатор филиала
        """
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = select(BranchSchemasTable).where(BranchSchemasTable.branch_id == branch_id)
                    res = await session.execute(query)
                    data = res.fetchone()
                    if data is not None:
                        print(data[0])
                        res_data = storage_schem.branches_schem.BranchPlanSchemaBase.model_validate(obj=data[0])
                        return res_data

        except Exception as _ex:
            logger.critical(f"Ошибка при извлечении данных схемы помещения branch_id: {branch_id} -> {_ex}")
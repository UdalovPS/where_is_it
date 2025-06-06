"""database/auth"""

from typing import TYPE_CHECKING
import uuid
from datetime import datetime
import os
import contextlib

from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.providers import get_driver
from libcloud.storage.types import (
    ContainerAlreadyExistsError,
    ObjectDoesNotExistError,
    Provider,
)
from sqlalchemy import text, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField, ImageField
from sqlalchemy_file.storage import StorageManager

from database.db_core import Base

if TYPE_CHECKING:
    from database.organizations.model import OrganizationsTable
    from database.branches.model import BranchesTable


# настраиваем хранилище
os.makedirs("./upload_dir", 0o777, exist_ok=True)
driver = get_driver(Provider.LOCAL)("./upload_dir")

with contextlib.suppress(ContainerAlreadyExistsError):
    driver.create_container(container_name="branch_schemas")

container = driver.get_container(container_name="branch_schemas")

StorageManager.add_storage("branch_schemas", container)


def custom_filename(attached_file):
    return f"user_{attached_file.entity.id}.jpg"


class BranchSchemasTable(Base):
    __tablename__ = "branch_schemas_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches_table.id", ondelete="CASCADE"), nullable=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations_table.id", ondelete="CASCADE"))
    content = Column(FileField(upload_storage="branch_schemas"))

    creator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    updator_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=True)
    update_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                onupdate=datetime.utcnow, nullable=True)

    organization = relationship("OrganizationsTable")
    branch = relationship("BranchesTable")
    creator = relationship("UsersTable", foreign_keys=[creator_id])
    updator = relationship("UsersTable", foreign_keys=[updator_id])

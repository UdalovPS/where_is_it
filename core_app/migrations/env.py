import urllib
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

from storage.database.db.postgres_alchemy.alchemy_core import Base

# import all models
from storage.database.db.postgres_alchemy.users import UsersTable
from storage.database.db.postgres_alchemy.organizations import OrganizationsTable
from storage.database.db.postgres_alchemy.countries import CountriesTable
from storage.database.db.postgres_alchemy.districts import DistrictsTable
from storage.database.db.postgres_alchemy.cities import CitiesTable
from storage.database.db.postgres_alchemy.branches import BranchesTable
from storage.database.db.postgres_alchemy.auth import AuthTokenTable
from storage.database.db.postgres_alchemy.branch_schemas import BranchSchemasTable
from storage.database.db.postgres_alchemy.shelves import ShelvesTable
from storage.database.db.postgres_alchemy.categories import CategoriesTable
from storage.database.db.postgres_alchemy.items import ItemsTable
from storage.database.db.postgres_alchemy.spots import SpotsTable
from storage.database.db.postgres_alchemy.frontend_service import FrontendServicesTable
from storage.database.db.postgres_alchemy.clients import ClientsTable
from storage.database.db.postgres_alchemy.client_location import ClientLocationTable

from config import DB_HOST, DB_NAME, DB_PORT, DB_PASS, DB_USER

# escape password so it fits into connection string
DB_PASS = urllib.parse.quote_plus(DB_PASS).replace("%", "%%")

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_PASS", DB_PASS)
config.set_section_option(section, "DB_USER", DB_USER)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

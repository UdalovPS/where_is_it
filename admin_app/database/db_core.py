from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base

import config

# Создаем URL для подключения к БД
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT or 5432,
    database=config.DB_NAME,
)

# Создаем базовый класс, от которого будут наследоваться все модели
Base = declarative_base()

# Создаем движок
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

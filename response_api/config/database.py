
import traceback

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from response_api.config.api import (DB_HOST, DB_NAME,
                                     DB_PASS, DB_PORT,
                                     DB_SCHEMA, DB_USER)
from response_api.util.api import exc_info

DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DB_URL, pool_pre_ping=True)

try:
    if not engine.dialect.has_schema(engine, DB_SCHEMA):
        engine.execute(CreateSchema(DB_SCHEMA))
except SQLAlchemyError:
    error = traceback.format_exception_only(*exc_info())
    logger.error("[-] ERROR DETECTED IN DATABASE")
    logger.error(f"[-] SQLALCHEMY: ERROR DETECTED IN THE ORM OR DATABASE. {error}")
    logger.error("[-] ERROR DETECTED IN DATABASE")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

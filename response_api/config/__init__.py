import traceback

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from response_api.config.database import SessionLocal, engine
from response_api.model.database import Base
from response_api.util.api import exc_info


def init_configuration():
    try:
        logger.level("RESPONSE", no=15, color="<green><green>")
        logger.level("LATENCY", no=15, color="<blue><bold>")
        logger.level("EXCEPTION", no=25, color="<red><bold>")
    except TypeError:
        pass
    # Database Table and schema.
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError:
        error = traceback.format_exception_only(*exc_info())
        logger.error("[-] ERROR DETECTED IN DATABASE")
        logger.error(f"[-] SQLALCHEMY: ERROR DETECTED IN THE ORM OR DATABASE. {error}")
        logger.error("[-] ERROR DETECTED IN DATABASE")


def get_db():
    """
    Dependency
        :return: SessionLocal
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

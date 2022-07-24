
import json

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, SmallInteger, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from response_api.config.api import TODO1, TODO2
from response_api.config.database import Base
from response_api.model.schema import Response


class FkSolutionsService(Base):
    __tablename__ = "fksolutions_service"
    __table_args__ = {"schema": "controller"}

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(30), unique=True)
    description = Column(String(50), default=TODO1)

    response_service = relationship(
        "ResponseService", back_populates="fksolutions_service")


class SystemClient(Base):
    __tablename__ = "system_client"
    __table_args__ = {"schema": "controller"}

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(20), unique=True)
    description = Column(String(50), default=TODO2)

    response_service = relationship(
        "ResponseService", back_populates="system_client")


class ResponseService(Base):
    __tablename__ = "response_service"
    __table_args__ = {"schema": "controller"}

    response_id = Column(BigInteger, primary_key=True, index=True)
    client_identifier = Column(String)
    response_status = Column(SmallInteger, default=0)
    response_service = Column(String, default="processing")
    response_number = Column(SmallInteger, default=0)
    by_tokens = Column(Boolean, default=False)

    create_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    fksolutions_service_id = Column(
        SmallInteger, ForeignKey("controller.fksolutions_service.id"))
    system_client_id = Column(
        SmallInteger, ForeignKey("controller.system_client.id"))

    fksolutions_service = relationship(
        "FkSolutionsService", back_populates="response_service")
    system_client = relationship(
        "SystemClient", back_populates="response_service")

    def get_value(self):
        return Response(
            token_service=str(self.response_id),
            client_identifier=self.client_identifier,
            response_service=self.get_dict_response_service(),
            response_status=self.response_status
        )

    def get_dict_response_service(self):
        if self.response_service != 'processing':
            response = json.loads(self.response_service)
        else:
            response = {}
        return response

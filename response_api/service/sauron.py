import json
import traceback

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from response_api.exception.exc import (SQLAlchemyException,
                                        UniqueException)
from response_api.model.database import ResponseService
from response_api.model.schema import (
    ResponseServiceCreate, ResponseServiceUpdate)
from response_api.util.api import exc_info

from . import ServiceBase


class FkSolutions(ServiceBase):

    def create_response(self, schema: ResponseServiceCreate) -> int:
        try:
            system_client = self.system_repo.find_by_name(
                client_name=schema.system_client_name)
            fksolutions_service = self.service_repo.find_by_name(
                service_name=schema.fksolutions_service_name)

            response_service = ResponseService(
                response_id=self.response_repo.generate_id(),
                client_identifier=schema.system_client_identifier,
                system_client_id=system_client.id,
                fksolutions_service_id=fksolutions_service.id
            )
            response_service = self.response_repo.save(response_service)
            return response_service.response_id
        except IntegrityError:
            raise UniqueException(
                stacktrace=traceback.format_exception_only(*exc_info()))
        except SQLAlchemyError:
            raise SQLAlchemyException(
                stacktrace=traceback.format_exception_only(*exc_info()))

    def update_response(self, schema: ResponseServiceUpdate) -> None:
        try:
            self.response_repo.update_response(
                schema.response_id,
                json.dumps(schema.response_service),
                schema.response_status
            )
        except SQLAlchemyError:
            raise SQLAlchemyException(
                stacktrace=traceback.format_exception_only(*exc_info()))

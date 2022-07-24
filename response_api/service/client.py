
import traceback
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from response_api.exception.exc import (
    SQLAlchemyException, TokenServiceException)
from response_api.model.schema import (Response,
                                       ResponseBatchInput)
from response_api.util.api import exc_info

from . import ServiceBase


class Client(ServiceBase):

    def find_all_by_batch(self, schema: ResponseBatchInput) -> (List[Response], bool):
        try:
            if schema.response_number > 0:
                schema.response_number = self.response_repo.find_max_response_number_by_system_and_service(
                    schema.system_client_name, schema.fksolutions_service_name)
            # Set query
            response_db = self.response_repo.find_all_by_system_and_service(
                schema.system_client_name, schema.fksolutions_service_name, schema.response_number)
            return self.__get_response(response_db, schema)
        except SQLAlchemyError:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info()))

    def find_by_token(self, token_service: int, client_identifier: str) -> (Response, bool):
        try:
            response = self.response_repo.find_by_token(token_service, client_identifier)
            if not response:
                raise TokenServiceException()
            response_in_progress = False

            if response.ResponseService.response_number == 0:
                if response.response_status > 0:
                    self.update_number_of_response(response.ResponseService.response_number, response, True)
                else:
                    response_in_progress = True
            return response, response_in_progress
        except SQLAlchemyError:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info()))

    def update_number_of_response(self, response_number, response_db, by_token: bool = False):
        try:
            if response_number == 0:
                # Update response number for new a responses
                if not by_token:
                    self.response_repo.update_response_number(response_db)
                else:
                    self.response_repo.update_by_token_response_number(response_db.ResponseService.response_id)
        except SQLAlchemyError:
            raise SQLAlchemyException(stacktrace=traceback.format_exception_only(*exc_info()))

    def __get_response(self, response_db, schema: ResponseBatchInput):
        response = list()
        response_in_progress = self.response_repo.count_in_progress_by_system_and_service(
            schema.system_client_name, schema.fksolutions_service_name)

        if response_db:  # Get ended responses
            response = [res.ResponseService.get_value() for res in response_db]
            self.update_number_of_response(schema.response_number, response_db)
        return response, response_in_progress

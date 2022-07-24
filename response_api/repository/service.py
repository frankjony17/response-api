
from datetime import date

from sqlalchemy import func

from response_api.model.database import (ResponseService,
                                         FkSolutionsService,
                                         SystemClient)

from . import Repository


class ResponseServiceRepository(Repository):

    fields = ('response_id', 'client_identifier', 'response_service', 'response_status')

    def generate_id(self) -> int:
        today = date.today()
        response_id = self.db.query(func.max(ResponseService.response_id)).filter(
            func.DATE(ResponseService.create_at) == today
        ).scalar()
        if response_id is None or response_id == 0:
            response_id = int(f"{today.strftime('%Y%m%d')}0000000")
        return response_id + 1

    def update_response(self, response_id: int, response_service: str, response_status: int) -> None:
        self.update(
            ResponseService,
            response_id,
            {"response_service": response_service,
             "response_status": response_status}
        )

    def find_all_by_system_and_service(self, client_name: str, service_name: str, resp_number: int):
        return self.db.query(
            ResponseService, *self.fields
        ).join(
            SystemClient, SystemClient.client_name == client_name
        ).join(
            FkSolutionsService, FkSolutionsService.service_name == service_name
        ).filter(
            ResponseService.response_number == resp_number,
            ResponseService.response_status != int(0)
        ).all()

    def count_in_progress_by_system_and_service(self, client_name: str, service_name: str):
        return self.db.query(
            ResponseService, *self.fields
        ).join(SystemClient).filter(
            SystemClient.client_name == client_name
        ).join(FkSolutionsService).filter(
            FkSolutionsService.service_name == service_name
        ).filter(
            ResponseService.response_service == "processing"
        ).count()

    def update_response_number(self, response) -> None:
        response_number = self.find_max_response_number()
        for res in response:
            resp_id = res.ResponseService.response_id
            self.update(ResponseService, resp_id, {"response_number": int(response_number + 1)}, False)
        self.db.commit()

    def find_by_token(self, token_service: str, client_identifier: str) -> ResponseService:
        return self.db.query(
            ResponseService, *self.fields
        ).join(SystemClient).filter(
            SystemClient.client_name == client_identifier
        ).filter(
            ResponseService.response_id == int(token_service)
        ).first()

    def update_by_token_response_number(self, response_id: int) -> None:
        response_number = self.find_max_response_number()
        self.update(
            ResponseService, response_id, {"response_number": int(response_number + 1), "by_tokens": True})

    def find_max_response_number(self) -> int:
        return self.db.query(func.max(ResponseService.response_number)).scalar()

    def find_max_response_number_by_system_and_service(self, client_name: str, service_name: str) -> int:
        return self.db.query(
            func.max(ResponseService.response_number)
        ).join(SystemClient).filter(
            SystemClient.client_name == client_name
        ).join(FkSolutionsService).filter(
            FkSolutionsService.service_name == service_name
        ).scalar()


class FkSolutionsServiceRepository(Repository):
    def find_by_name(self, service_name: str) -> FkSolutionsService:
        service = self.db.query(FkSolutionsService).filter(
            FkSolutionsService.service_name == service_name).first()
        if not service:
            service = self.save(FkSolutionsService(service_name=service_name))
        return service


class SystemClientRepository(Repository):
    def find_by_name(self, client_name: str) -> SystemClient:
        service = self.db.query(SystemClient).filter(
            SystemClient.client_name == client_name).first()
        if not service:
            service = self.save(SystemClient(client_name=client_name))
        return service

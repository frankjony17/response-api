
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from response_api.config import get_db
from response_api.exception.exc import NotResponseException
from response_api.model.schema import (ResponseBatchInput,
                                       ResponseBatchOutput,
                                       ResponseByTokenInput,
                                       ResponseByTokenOutput)
from response_api.service.client import Client

route_client = APIRouter()


@route_client.post('/response/get-by-batch',
                   summary='Obter lote de respostas registradas.',
                   status_code=200,
                   response_model=ResponseBatchOutput)
def get_by_batch(data: ResponseBatchInput, response: Response, db: Session = Depends(get_db)):
    service = Client(db)
    response_service, response_in_progress = service.find_all_by_batch(data)

    if len(response_service) == 0:
        if response_in_progress > 0:
            response.status_code = status.HTTP_206_PARTIAL_CONTENT
        else:
            raise NotResponseException()

    return ResponseBatchOutput(
        system_client_name=data.system_client_name,
        fksolutions_service_name=data.fksolutions_service_name,
        response_service=response_service,
        response_in_progress=response_in_progress
    )


@route_client.post('/response/get-by-token',
                   summary='Obter resposta registrada pelo identificador de token.',
                   status_code=200,
                   response_model=ResponseByTokenOutput)
def get_by_token(data: ResponseByTokenInput, response: Response, db: Session = Depends(get_db)):
    service = Client(db)
    response_service, response_in_progress = service.find_by_token(int(data.token_service), data.client_identifier)

    if response_in_progress:
        response.status_code = status.HTTP_206_PARTIAL_CONTENT

    return ResponseByTokenOutput(
        token_service=response_service.response_id,
        client_identifier=response_service.client_identifier,
        response_service=response_service.ResponseService.get_dict_response_service(),
        response_status=response_service.response_status,
        response_in_progress=response_in_progress
    )

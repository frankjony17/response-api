
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from response_api.config import get_db
from response_api.model.schema import (
    ResponseServiceCreate, ResponseServiceOutput, ResponseServiceUpdate,
    ResponseServiceUpdateOutput)
from response_api.service.fksolutions import FkSolutions

route_fksolutions = APIRouter()


@route_fksolutions.post('/response/create',
                   summary='Criar entrada da resposta do serviço',
                   status_code=200,
                   response_model=ResponseServiceOutput)
def create_first(data: ResponseServiceCreate, db: Session = Depends(get_db)):
    controller_service = FkSolutions(db)
    response_id = controller_service.create_response(data)
    return ResponseServiceOutput(fksolutions_response_id=response_id)


@route_fksolutions.post('/response/update',
                   summary='Atualizar resposta do serviço registrado',
                   status_code=200,
                   response_model=ResponseServiceUpdateOutput)
def update_service(data: ResponseServiceUpdate, db: Session = Depends(get_db)):
    controller_service = FkSolutions(db)
    controller_service.update_response(data)
    return ResponseServiceUpdateOutput(success=True)

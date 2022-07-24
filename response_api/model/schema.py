
from typing import List

from pydantic import BaseModel


class ResponseBase(BaseModel):
    system_client_name: str
    fksolutions_service_name: str


class FkSolutionsServiceCreate(BaseModel):
    service_name: str


class SystemClientCreate(BaseModel):
    client_name: str


class ResponseServiceCreate(ResponseBase):
    system_client_identifier: str


class ResponseServiceUpdate(BaseModel):
    response_id: int
    response_service: dict
    response_status: int


class ResponseServiceOutput(BaseModel):
    fksolutions_response_id: int


class ResponseServiceUpdateOutput(BaseModel):
    success: bool


class Response(BaseModel):
    token_service: str
    client_identifier: str
    response_service: dict
    response_status: int


class ResponseBatchOutput(ResponseBase):
    response_service: List
    response_in_progress: int


class ResponseByTokenOutput(Response):
    response_in_progress: bool


class ResponseBatchInput(ResponseBase):
    response_number: int


class ResponseByTokenInput(BaseModel):
    token_service: str
    client_identifier: str

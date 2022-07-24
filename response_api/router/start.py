
from fastapi import APIRouter

start = APIRouter()


@start.get('/', summary="Welcome to to FkSolutions Response Controller API",
           status_code=200)
def welcome():
    return 'Welcome to FkSolutions Response Controller API, ' \
           'read documentation in /docs for further questions.'


@start.get('/health', summary="API is stand up?", status_code=200)
def health():
    return 'UP'

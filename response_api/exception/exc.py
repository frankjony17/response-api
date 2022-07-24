
from loguru import logger


class APiException(Exception):
    def __init__(self, stacktrace: str = ":)", code: int = 404,
                 message: str = "OPERATION ERROR"):
        self.code = code
        self.message = message
        self.stacktrace = stacktrace
        logger.log("EXCEPTION", f'[-] {message}, STATUS: {code}')


class UniqueException(APiException):
    def __init__(self, stacktrace):
        message = 'UNIQUE CONSTRAINT: THE VALUE ALREADY EXISTS IN THE DATABASE'
        super().__init__(stacktrace, 409, message)


class SQLAlchemyException(APiException):
    def __init__(self, stacktrace):
        message = 'SQLALCHEMY: ERROR DETECTED IN THE ORM OR DATABASE'
        super().__init__(stacktrace, 444, message)


class TokenServiceException(APiException):
    def __init__(self):
        message = 'NO SERVICE WAS REGISTERED WITH THAT TOKEN. TOKEN NONEXISTENT'
        super().__init__(code=404, message=message)


class NotResponseException(APiException):
    def __init__(self):
        message = 'THERE IS NO REGISTERED RESPONSE FOR THIS CLIENT OR SERVICE'
        super().__init__(code=404, message=message)

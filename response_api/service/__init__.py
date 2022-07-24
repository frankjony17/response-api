
from sqlalchemy.orm import Session

from response_api.repository import service


class ServiceBase:

    def __init__(self, session: Session):
        self.system_repo = service.SystemClientRepository(session)
        self.service_repo = service.FkSolutionsServiceRepository(session)
        self.response_repo = service.ResponseServiceRepository(session)

    def __del__(self):
        del self.system_repo
        del self.service_repo
        del self.response_repo

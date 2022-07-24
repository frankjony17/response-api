from sqlalchemy.orm import Session

from response_api.config.database import Base
from response_api.model.database import ResponseService


class Repository:

    def __init__(self, session: Session):
        self.db = session

    def save(self, model: Base):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: Base, model_id: int, values: dict, commit: bool = True):
        if model == ResponseService:
            self.db.query(model).filter(model.response_id == model_id).update(values)
        else:
            self.db.query(model).filter(model.id == model_id).update(values)
        self.db.commit() if commit else None

    def __del__(self):
        del self.db

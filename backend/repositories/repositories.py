from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db_session: Session, model):
        self.db_session = db_session
        self.model = model

    def get_by(self, **kwargs):
        return self.db_session.query(self.model).filter_by(**kwargs).first()

    def get_all(self):
        return self.db_session.query(self.model).all()

    def get_all_by(self, **kwargs):
        return self.db_session.query(self.model).filter_by(**kwargs).all()

    def create(self, data: dict):
        instace = self.model(**data)
        self.db_session.add(instace)
        self.db_session.commit()
        self.db_session.refresh(instace)
        return instace

    def update(self, instance, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        self.db_session.commit()
        self.db_session.refresh(instance)
        return instance

    def delete(self, instance):
        self.db_session.delete(instance)
        self.db_session.commit()
        return True

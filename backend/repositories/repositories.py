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

    def get_all_paginated(self, page: int = 1, per_page: int = 10, order_by_col: str = "id", order_desc: bool = True):
        base_query = self.db_session.query(self.model)
        
        total = base_query.count()
        
        order_column = getattr(self.model, order_by_col, self.model.id)
        if order_desc:
            order_column = order_column.desc()
        
        offset = (page - 1) * per_page
        
        instances = (
            base_query
            .order_by(order_column)
            .offset(offset)
            .limit(per_page)
            .all()
        )
        
        return instances, total
    
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

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, msg=None):
        from app.libs.error_code import NotFound

        rv = self.get(ident)
        if not rv or rv.status != 1:
            raise NotFound(msg=msg)
        return rv

    def first_or_404(self, msg=None):
        from app.libs.error_code import NotFound

        rv = self.first()
        if not rv or rv.status != 1:
            raise NotFound(msg=msg)
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    # def to_dict(self):
    #     return {c.name: getattr(self, c.name, None)
    #             for c in self.__table__.columns}

    def to_dict(self):
        return {
            column_name: getattr(self, column_name, None)
            for column_name in self.fields
        }

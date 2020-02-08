from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager
from time import time
from datetime import datetime

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
        """重写filter_by 方法，默认status=1"""
        if "status" not in kwargs.keys():
            kwargs["status"] = 1
        return super().filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True                         # 模型基类声明
    _create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self._create_time = time()

    def delete(self):
        """假删除"""
        self.status = 0

    def __getitem__(self, key):
        """实现dict取值"""
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != "ID":
                setattr(self, k, v)

    @property
    def create_time(self):
        return datetime.fromtimestamp(self._create_time)

    @create_time.setter
    def create_time(self, caw):
        self._create_time = float(caw)

# from . import book, user, gift, wish

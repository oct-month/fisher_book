from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger
from sqlalchemy.orm import relationship
from flask import current_app

from app.spider.fishbook import YushuBook

from . import Base

class Gift(Base):
    """赠送的数据库"""
    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID
    launched = Column(Boolean, default=False)                   # 赠送状态

    isbn = Column(String(15), nullable=False)                   # 书的isbn

    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.ID"))               # 用户ID

    @property
    def book(self):
        yu_book = YushuBook()
        yu_book.search_by_isbn(self.isbn)
        return yu_book.first

    @classmethod
    def recent(cls):
        """查询最近的礼物"""
        recent_gift = cls.query.filter_by(launched=False).order_by(
                cls._create_time).group_by(cls.isbn).distinct().limit(
                current_app.config["RECENT_BOOK_COUNT"]).all()
        return recent_gift

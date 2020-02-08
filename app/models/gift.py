from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship
from flask import current_app
from collections import defaultdict

from app.spider.fishbook import YushuBook

from . import Base, db

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

    def is_yourself_gift(self, uid):
        """判断当前的gift是不是uid的"""
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = cls.query.filter_by(uid=uid, launched=False).order_by(
            desc(cls._create_time)).all()
        return gifts

    @classmethod
    def recent(cls):
        """查询最近的礼物"""
        recent_gift = cls.query.filter_by(launched=False).order_by(
                desc(cls._create_time)).group_by(cls.isbn).distinct().limit(
                current_app.config["RECENT_BOOK_COUNT"]).all()
        return recent_gift

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        """根据传入的一组isbn，计算出每一个isbn的wish数量"""
        gifts_count = db.session.query(cls.isbn, func.count(cls.ID)).filter(cls.status==1, 
            cls.launched == False, cls.isbn.in_(isbn_list)).group_by(cls.isbn).all()
        count_dict = defaultdict(int)         # isbn为键
        for w in gifts_count:
            count_dict[w[0]] += w[1]
        return count_dict

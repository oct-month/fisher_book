from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, func, desc
from sqlalchemy.orm import relationship
from collections import defaultdict

from app.spider.fishbook import YushuBook

from . import Base, db

class Wish(Base):
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
    def get_user_wishes(cls, uid):
        """获取用户的全部wish"""
        wishes = cls.query.filter_by(uid=uid, launched=False).order_by(
            desc(cls._create_time)).all()
        return wishes

    @classmethod
    def get_wish_count(cls, isbn_list):
        """根据传入的一组isbn，计算出每一个isbn的wish数量"""
        wishes_count = db.session.query(cls.isbn, func.count(cls.ID)).filter(cls.status==1, 
            cls.launched == False, cls.isbn.in_(isbn_list)).group_by(cls.isbn).all()
        count_dict = defaultdict(int)         # isbn为键
        for w in wishes_count:
            count_dict[w[0]] += w[1]
        return count_dict
        #return dict(wishes_count)

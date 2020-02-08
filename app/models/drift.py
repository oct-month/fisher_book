from sqlalchemy import Column, Integer, String, SmallInteger
from flask_login import current_user

from app.view.book import BookView

from . import Base, db

class Drift(Base):
    """一次具体的交易信息"""
    ID = Column(Integer, primary_key=True, autoincrement=True)
    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)         # 收件人
    address = Column(String(100), nullable=False)               # 地址
    message = Column(String(200))                               # 留言
    mobile = Column(String(20), nullable=False)                 # 手机号
    # 书籍信息
    isbn = Column(String(13))                                   # 书的isbn
    book_title = Column(String(50))                             # 书名
    book_author = Column(String(30))                            # 作者
    book_img = Column(String(50))                               # 书的图片
    # 请求者信息
    requester_id = Column(Integer)                              # 请求者ID
    requester_nickname = Column(String(20))                     # 请求者昵称
    # 赠送者信息
    gifter_id = Column(Integer)                                 # 赠送者ID
    gift_id = Column(Integer)                                   # 礼物ID
    gifter_nickname = Column(String(20))                        # 赠送者昵称
    # 状态
    pending = Column(SmallInteger, default=1)

    @classmethod
    def save_drift(cls, drift_form, current_gift):
        """根据表单和gift保存drift"""
        with db.auto_commit():
            drift = cls()
            drift_form.populate_obj(drift)  # 表单的属性赋值方法
            drift.gift_id = current_gift.ID
            drift.requester_id = current_user.ID
            drift.requester_nickname = current_user.nickname
            drift.gifter_id = current_gift.user.ID
            drift.gifter_nickname = current_gift.user.nickname
            book = BookView(current_gift.book)
            drift.book_title = book.title
            drift.book_author = book.author
            drift.book_img = book.image
            drift.isbn = book.isbn
            current_user.beans -= 1
            db.session.add(drift)

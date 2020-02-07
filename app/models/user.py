from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.web import login_manager
from app.spider.fishbook import YushuBook
from app.models.gift import Gift
from app.models.wish import Wish
from app.libs.judge import str_is_ISBN

from . import Base

class User(Base, UserMixin):
    """用户的数据库"""
    __tablename__ = "user"

    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID
    nickname = Column(String(24), nullable=False)               # 昵称
    _password = Column("password", String(128), nullable=False)
    phone_number = Column(String(18), unique=True)              # 电话
    email = Column(String(50), unique=True, nullable=False)     # 邮件
    confirmed = Column(Boolean, default=False)                  #
    beans = Column(Float, default=0)                            # 鱼豆
    send_counter = Column(Integer, default=0)                   #
    receive_counter = Column(Integer, default=0)                # 
    # 日后开发微信使用
    wx_open_id = Column(String(50))                             #
    wx_name = Column(String(32))                                #

    @property
    def password(self):
        return self._password

    @password.setter                                            # 赋值
    def password(self, raw):
        """加密保存密码"""
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """检查密码"""
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        # isbn 不合法
        if not str_is_ISBN(isbn):
            return False
        yu_book = YushuBook()
        yu_book.search_by_isbn(isbn)
        # isbn 不存在
        if not yu_book.first:
            return False
        # 既不在赠送清单中，也不再心愿清单中才能添加
        gift = Gift.query.filter_by(uid=self.ID, isbn=isbn, launched=False).first()
        wish = Wish.query.filter_by(uid=self.ID, isbn=isbn, launched=False).first()
        if gift or wish:
            return False
        return True
    
    def get_id(self):
        """flask_login 使用"""
        return self.ID

@login_manager.user_loader
def get_user(uid):
    """返回 current_user"""
    return User.query.get(int(uid))
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.web import login_manager
from app.spider.fishbook import YushuBook
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift
from app.libs.judge import str_is_ISBN
from app.libs.enums import PendingStatus

from . import Base, db

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

    @property
    def summary(self):
        return {
            "nickname": self.nickname,
            "beans": self.beans,
            "email": self.email,
            "send_receive": str(self.send_counter) + "/" + str(self.receive_counter)
        }

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
    
    def can_send_drift(self):
        """判断当前用户能否索要书籍"""
        # 鱼豆 >= 1
        if self.beans < 1:
            return False
        # 每索取2本书，自己必须送出一本书
        success_gift_count = Gift.query.filter_by(uid=self.ID, launched=True).count()
        success_receice_count = Drift.query.filter_by(requester_id=self.ID, pending=PendingStatus.Success).count()
        return True if success_receice_count // 2 <= success_gift_count else False

    def generate_token(self, expiration=600):       # 过期时间设置为10分钟
        """生成一个加密过的ID"""
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        temp = s.dumps({"id": self.ID})     # 返回bytes
        return temp.decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception:
            return False
        uid = data.get("id")    # 查询主键
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True
    
    def get_id(self):
        """flask_login 使用"""
        return self.ID

@login_manager.user_loader
def get_user(uid):
    """返回 current_user"""
    return User.query.get(int(uid))

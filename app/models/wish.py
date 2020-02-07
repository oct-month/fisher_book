from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger
from sqlalchemy.orm import relationship

from . import Base

class Wish(Base):
    """赠送的数据库"""
    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID
    launched = Column(Boolean, default=False)                   # 赠送状态

    isbn = Column(String(15), nullable=False)                   # 书的isbn

    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.ID"))               # 用户ID

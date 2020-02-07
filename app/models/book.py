# 模型层（数据库）
# Code first 专注业务模型的设计，而不是专注数据库的设计
from sqlalchemy import Column, Integer, String
from . import Base

class Book(Base):
    """书的数据库"""
    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID
    title = Column(String(50), nullable=False)                  # 书名
    author = Column(String(30), default="佚名")                 # 作者
    isbn = Column(String(15), nullable=False, unique=True)      # ISBN
    binding = Column(String(20))                                # 装帧（精装）
    publisher = Column(String(50))                              # 出版社
    price = Column(String(20))                                  # 价格
    pages = Column(Integer)                                     # 页数
    pubdate = Column(String(20))                                # 出版年月
    summary = Column(String(1000))                              # 简介
    image = Column(String(50))                                  # 图片

    @classmethod
    def search_by_isbn(cls, isbn):
        book = cls.query.filter_by(isbn=isbn).first()
        return book

    def fill_by_bookdict(self, book_dict):
        """填充书籍信息"""
        self.title = book_dict["title"]
        self.publisher = book_dict["publisher"]
        self.author = "、".join(book_dict["author"])
        self.image = book_dict["image"]
        self.price = book_dict["price"]
        self.summary = book_dict["summary"]
        self.pages = book_dict["pages"]
        self.isbn = book_dict["isbn"]
        self.pubdate = book_dict["pubdate"]
        self.binding = book_dict["binding"]

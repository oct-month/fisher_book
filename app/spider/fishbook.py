from flask import current_app
from app.libs.internet import HTTP
from app.models import db
from app.models.book import Book

class YushuBook:

    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        """根据isbn查找书籍信息"""
        result = Book.search_by_isbn(isbn)
        if not result:
            url = self.isbn_url.format(isbn)
            result = HTTP.get(url)
            # 插入数据库
            tap = Book()
            tap.fill_by_bookdict(result)
            with db.auto_commit():
                db.session.add(tap)
        else:
            result.author = result.author.split("、")

        self.__fill_single(result)


    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.caculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total += 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total += data["total"]
        self.books.extend(data["books"])

    @property
    def first(self):
        """返回查询结果的第一条"""
        return self.books[0] if self.total >= 1 else None

    @staticmethod
    def caculate_start(page):
        return (page-1) * current_app.config["PER_PAGE"]

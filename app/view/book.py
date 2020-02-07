
class BookView:
    """处理单本数据"""
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.author = "、".join(book["author"])
        self.image = book["image"]
        self.price = book["price"]
        self.summary = book["summary"]
        self.pages = book["pages"]
        self.isbn = book["isbn"]
        self.pubdate = book["pubdate"]
        self.binding = book["binding"]
    
    @property
    def intro(self):
        intros = filter(lambda x:True if x else False, [self.author, self.publisher, self.price])
        return "/".join(intros)

class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ""
    
    def fill(self, fishbook, keyword):
        self.total = fishbook.total
        self.books = [BookView(book) for book in fishbook.books]
        self.keyword = keyword

        



    # @classmethod
    # def package_single(cls, data, keyword):
    #     """处理isbn 搜索时返回的数据"""
    #     result = {
    #         "books": [],
    #         "total": 0,
    #         "keyword": ""
    #     }
    #     if data:
    #         result["total"] = 1
    #         result["books"] = [cls.__cut_book_data(data)]
    #     return result
        
    # @classmethod
    # def package_collection(cls, data, keyword):
    #     """处理关键字 搜索时返回的数据"""
    #     result = {
    #         "books": [],
    #         "total": 0,
    #         "keyword": keyword
    #     }
    #     if data:
    #         result["total"] = len(data["total"])
    #         result["books"] = [cls.__cut_book_data(book) for book in data["books"]]
    #     return result

    # @classmethod
    # def __cut_book_data(cls, data):
    #     """处理book 数据"""
    #     book = {
    #         "title": data["title"] or "",
    #         "author": "、".join(data["author"]),
    #         "publisher": data["publisher"] or "",
    #         "price": data["price"] or 0,
    #         "summary": data["summary"] or "",
    #         "image": data["image"]
    #     }
    #     return book



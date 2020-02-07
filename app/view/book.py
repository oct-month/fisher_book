
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



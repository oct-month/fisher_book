from .book import BookView


class MyWishes:
    def __init__(self, wishs_of_mine, wishes_count_dict):
        self.wishs = []
        self.__wishs = wishs_of_mine
        self.__wishes = wishes_count_dict
        self.wishs = self.__parse()
    
    def __parse(self):
        temp = []
        for wish in self.__wishs:
            mywish = self.__match(wish)
            temp.append(mywish)
        return temp

    def __match(self, wish):
        """处理单个wish"""
        r = {
            "id": wish.ID,
            "book": BookView(wish.book),
            "wishes_count": self.__wishes[wish.isbn]
        }
        return r

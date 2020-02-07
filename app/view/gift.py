from .book import BookView


class MyGifts:
    def __init__(self, gifts_of_mine, wishes_count_dict):
        self.gifts = []
        self.__gifts = gifts_of_mine
        self.__wishes = wishes_count_dict
        self.gifts = self.__parse()
    
    def __parse(self):
        temp = []
        for gift in self.__gifts:
            mygift = self.__match(gift)
            temp.append(mygift)
        return temp

    def __match(self, gift):
        """处理单个gift"""
        r = {
            "id": gift.ID,
            "book": BookView(gift.book),
            "wishes_count": self.__wishes[gift.isbn]
        }
        return r

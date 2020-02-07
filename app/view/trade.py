from time import time

class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)
    
    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        """处理单个数据"""
        return {
            "user_name": single.user.nickname,
            "time": single.create_time.strftime("%Y-%m-%d"),
            "id": single.ID
        }


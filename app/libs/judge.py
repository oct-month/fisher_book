"""
执行各种判断
"""
import re

def str_is_ISBN(my_str):
    """判断传入的str 是不是ISBN"""
    # 例如：ISBN9787111606598
    # isbn13 : 13个0到9的数字组成
    # isbn10 : 10个0到9的数字组成，含有一些 '-'
    my_str = my_str.strip()
    if re.match("^(ISBN)?\s*?\d{10,13}$", my_str.replace("-", ""), re.I):
        return True 
    return False


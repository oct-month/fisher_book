# with 的另一种构建方式
from contextlib import contextmanager

class Demo:
    def query(self):
        print("query")

@contextmanager
def work():
    print("open")
    yield Demo()
    print("close")

with work() as r:
    r.query()

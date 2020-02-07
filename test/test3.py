from threading import Thread, local
from werkzeug.local import Local

# 线程隔离对象Local
a = Local()
a.index = 0

def work():
    a.index = 2
    print(a, a.index)

t = Thread(target=work, name="秀")
t.start()

print(a, a.index)

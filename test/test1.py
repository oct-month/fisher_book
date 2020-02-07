from flask import Flask, current_app

app = Flask(__name__)

# 离线应用、单元测试

ctx = app.app_context()
ctx.push()
a = current_app
print(a.config, app == a)
ctx.pop()

# with + 上下文表达式   写法：
with app.app_context():
    a = current_app
    print(a.config, app == a)
# 实现了上下文协议的对象使用with
# 实现了上下文协议的对象：上下文管理器
# 实现了__enter__ 和 __exit__
# 上下文表达式必须要返回一个上下文管理器

class Test:
    def __enter__(self):
        a = {"a": 3}
        print(a)
        return self
    
    def __exit__(self, exc_type, exc_value, tb):    # 错误类，错误类的对象，traceback对象
        print(exc_type, exc_value, tb)
        print(type(exc_type), type(exc_value), type(tb))
        return True     # 返回True则不会抛出异常，返回False会在with外部抛出异常

with Test() as A:
    print(A)
    a = 1/0
    print(a)    # 始终不会执行

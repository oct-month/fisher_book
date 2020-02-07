"""
flask 主程序
"""
from flask import Flask, jsonify
from judge import str_is_ISBN
from book import YushuBook

app = Flask(__name__)
app.config.from_object("config")    # 导入配置文件

@app.route("/index/")       # 兼容末尾不带 / 的请求（重定向，因为要保证唯一url）
def index():
    return "Hello world"

app.add_url_rule("/", view_func=index)  # 另一种路由注册方式

# url -> endpoint -> function
@app.route("/book/search/<q>/<page>")
def search(q, page):
    """搜索API"""
    q = q.strip()
    if str_is_ISBN(q):
        book_dict = YushuBook.search_by_isbn(q)
    else:
        book_dict = YushuBook.search_by_keyword(q)
    return jsonify(book_dict)
    # dict 序列化（相当于：return json.dumps(book_dict), 200, {"content-type": "application/json"}）


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])   # 读取配置文件中的参数

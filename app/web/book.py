"""
蓝图
"""
from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.judge import str_is_ISBN
from app.spider.fishbook import YushuBook
from app.view.book import BookView, BookCollection
from app.view.trade import TradeInfo
from app.models.gift import Gift
from app.models.wish import Wish

from . import web

@web.route("/book/search/")
def search():
    """搜索API"""
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data
        page = form.page.data
        q = q.strip()

        yubook = YushuBook()
        if str_is_ISBN(q):
            yubook.search_by_isbn(q)
        else:
            yubook.search_by_keyword(q, page)

        books.fill(yubook, q)
        # return jsonify(books)
        # dict 序列化（相当于：return json.dumps(books), 200, {"content-type": "application/json"}）
    else:
        flash("搜索的关键字不符合要求")
    return render_template("search_result.html", books=books)

@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gifts = False        # 该书在不在gift清单中
    has_in_wishes = False       # 该书在不在wish清单中

    yu_book = YushuBook()
    yu_book.search_by_isbn(isbn)
    book = BookView(yu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.ID, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.ID, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template("book_detail.html", 
                            book=book, 
                            wishes=trade_wishes_model, 
                            gifts=trade_gifts_model,
                            has_in_gifts=has_in_gifts,
                            has_in_wishes=has_in_wishes)

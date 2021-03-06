from flask import render_template

from app.models.gift import Gift
from app.view.book import BookView

from . import web


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookView(gift.book) for gift in recent_gifts]
    return render_template("index.html", recent=books)

@web.route('/personal')
def personal_center():
    pass

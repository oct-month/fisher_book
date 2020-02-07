from flask import render_template
from flask_login import login_required, current_user

from app.models import db
from app.models.wish import Wish
from app.models.gift import Gift
from app.view.wish import MyWishes
from . import web

@web.route('/my/wish')
def my_wish():
    uid = current_user.ID
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    count_list = Gift.get_gifts_counts(isbn_list)
    view_module = MyWishes(wishes_of_mine, count_list)
    return render_template("my_wish.html", wishes=view_module.wishs)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.ID
            db.session.add(wish)


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass

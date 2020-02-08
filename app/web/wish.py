from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import db
from app.models.wish import Wish
from app.models.gift import Gift
from app.view.wish import MyWishes
from app.libs.email import send_email

from . import web

@web.route('/my/wish')
@login_required
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
    """添加到心愿单"""
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.ID
            db.session.add(wish)
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """向别人赠送书籍"""
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.ID, isbn=wish.isbn).first()
    if not gift:
        flash("你还没有上传此书。\n请点击“加入到赠送清单”添加此书")
    else:
        send_email(wish.user.email, "有人想送你一本书", "email/satisify_wish.html", wish=wish, gift=gift)
        flash("已向他/她发送了一封邮件，如果他/她接受，你将收到一个鱼漂")
    return redirect(url_for("web.book_detail", isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    """撤销心愿"""
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for("web.my_wish"))

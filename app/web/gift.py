from flask_login import login_required, current_user
from flask import current_app, flash, redirect, url_for, render_template

from app.models import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift
from app.view.gift import MyGifts
from app.libs.enums import PendingStatus

from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    """查看我的gift"""
    uid = current_user.ID
    gift_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gift_of_mine]
    wish_count_dict = Wish.get_wish_count(isbn_list)
    view_module = MyGifts(gift_of_mine, wish_count_dict)
    return render_template("my_gifts.html", gifts=view_module.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.ID
            current_user.beans += current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(gift)
    else:
        flash("这本书已存在于你的赠送清单或心愿清单中")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    """撤销礼物"""
    gift = Gift.query.filter_by(ID=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash("这个礼物正处于等待状态，请先往鱼漂处理")
    else:
        with db.auto_commit():
            gift.delete()
            current_user.beans -= current_app.config["BEANS_UPLOAD_ONE_BOOK"]
    return redirect(url_for("web.my_gifts"))


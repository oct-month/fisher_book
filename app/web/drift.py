from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from app.models.gift import Gift
from app.models.drift import Drift
from app.forms.drift import DriftForm
from app.libs.email import send_email

from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """发起索要请求"""
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.ID):
        flash("不能向自己索要书籍")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template("not_enough_beans.html", beans=current_user.beans)
    gifter = current_gift.user.summary

    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        Drift.save_drift(form, current_gift)
        send_email(current_gift.user.email, "有人想要一本书", "email/get_gift.html", 
            wisher=current_user, gift=current_gift)
        return redirect("web.pending")
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass

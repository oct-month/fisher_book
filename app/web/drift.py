from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from app.models import db
from app.models.gift import Gift
from app.models.drift import Drift
from app.forms.drift import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.view.dirft import DriftCollection

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
        return redirect(url_for("web.pending"))
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    """查看交易记录"""
    drifts = Drift.query.filter(or_(Drift.requester_id==current_user.ID, 
        Drift.gifter_id==current_user.ID)).order_by(desc(Drift._create_time)).all()
    views = DriftCollection(drifts, current_user.ID)
    return render_template("pending.html", drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    drift = Drift.query.get_or_404(did)
    with db.auto_commit():
        drift.pending = PendingStatus.Redraw
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    pass

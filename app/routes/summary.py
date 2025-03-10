from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.create import CreateForm
from app.forms.update import UpdateForm
from app.forms.delete import DeleteForm
from app.models import Summary
from app.extensions import db

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        giver_name = form.giver_name.data
        amount = form.amount.data
        address = form.address.data
        tel = form.tel.data
        note = form.note.data

        flash("データが正常に作成されました！", "success")
        return redirect(url_for('summary.create'))

    return render_template('create.html', form=form)

@summary_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    summary = Summary.query.get_or_404(id)
    form = UpdateForm(obj=summary)

    if form.validate_on_submit():
        summary.giver_name = form.giver_name.data
        summary.amount = form.amount.data
        summary.address = form.address.data
        summary.tel = form.tel.data
        summary.note = form.note.data

        db.session.commit()
        flash("データが正常に更新されました！", "success")
        return redirect(url_for('summary.index'))

    return render_template('update.html', form=form)

@summary_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    summary = Summary.query.get_or_404(id)
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(summary)
        db.session.commit()
        flash("データが削除されました！", "success")
        return redirect(url_for('summary.index'))

    return render_template('delete.html', form=form, summary=summary)

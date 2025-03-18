from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from app.forms import SummaryForm
from app.forms import DeleteForm
from app.models import Summary
from app.extensions import db
from app.utils.summaries_helpers import database_reset

summaries_bp = Blueprint('summaries', __name__)

@summaries_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = SummaryForm()

    if form.validate_on_submit():
        try:
            new_entry = Summary(
                giver_name=form.giver_name.data,
                amount=form.amount.data,
                address=form.address.data,
                tel=form.tel.data,
                note=form.note.data
            )
            db.session.add(new_entry)
            db.session.commit()

            flash('データが正常に作成されました！', 'success')
            return redirect(url_for('summaries.create'))

        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'danger')
            return render_template('create.html', form=form)

    return render_template('create.html', form=form)

@summaries_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    summary = Summary.query.get_or_404(id)
    form = SummaryForm(obj=summary)

    if form.validate_on_submit():
        try:
            summary.giver_name = form.giver_name.data
            summary.amount = form.amount.data
            summary.address = form.address.data
            summary.tel = form.tel.data
            summary.note = form.note.data

            db.session.commit()

            flash('データが正常に更新されました！', 'success')
            return redirect(url_for('main.main'))

        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'danger')
            return render_template('update.html', form=form)

    return render_template('update.html', form=form)

@summaries_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    summary = Summary.query.get_or_404(id)
    form = DeleteForm()

    if form.validate_on_submit():
        try:
            db.session.delete(summary)
            db.session.commit()

            flash('データが削除されました！', 'success')
            return redirect(url_for('main.main'))

        except Exception as e:
            db.session.rollback()
            flash(f'削除中にエラーが発生しました: {str(e)}', 'danger')
            return render_template('delete.html', form=form, summary=summary)

    return render_template('delete.html', form=form, summary=summary)

@summaries_bp.route('/database_reset', methods=['POST'])
def reset_database_route():
    if database_reset():
        return jsonify({"message": "初期状態に戻りました"}), 200
    else:
        return jsonify({"error": "初期化に失敗しました"}), 500

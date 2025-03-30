from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)

from app.extensions import db
from app.forms import CSRFForm, DeleteForm, SummaryForm
from app.models import Summary
from app.utils.summaries_helpers import database_reset, handle_form_errors

summaries_bp = Blueprint('summaries', __name__)

@summaries_bp.route('/index')
def index():
    summaries = Summary.query.filter_by(user_cognito_id=session.get('user_cognito_id')).all()
    form = CSRFForm()
    return render_template('index.html', summaries=summaries, form=form)

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
                note=form.note.data,
                user_cognito_id=session.get('user_cognito_id')
            )

            db.session.add(new_entry)
            db.session.commit()

            flash('登録されました')
            return redirect(url_for('summaries.create'))

        except Exception:
            db.session.rollback()
            current_app.logger.exception('❌ 登録エラー')
            flash('登録に失敗しました')
            return render_template(
                'create.html',
                form=form,
                action=url_for('summaries.create'),
                submit_label='登録'
            )

    if form.errors:
        handle_form_errors(form)

    return render_template(
        'create.html',
        form=form,
        action=url_for('summaries.create'),
        submit_label='登録'
    )

@summaries_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_cognito_id = session.get('user_cognito_id')
    if not user_cognito_id:
        current_app.logger.error('❌ user_cognito_id 取得失敗（/update）')
        flash('編集にはログインが必要です')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()

    if not summary:
        current_app.logger.critical(f'💥 user_cognito_id 不一致（/update） - IP: {request.remote_addr}')
        flash('編集権限がありません')
        return redirect(url_for('main.main'))

    form = SummaryForm(obj=summary)

    if form.validate_on_submit():
        try:
            summary.giver_name = form.giver_name.data
            summary.amount = form.amount.data
            summary.address = form.address.data
            summary.tel = form.tel.data
            summary.note = form.note.data

            db.session.commit()

            flash('データが編集されました')
            return redirect(url_for('summaries.index'))

        except Exception:
            db.session.rollback()
            current_app.logger.exception('❌ 編集エラー')
            flash('編集に失敗しました')
            return render_template(
                'update.html',
                summary=summary,
                form=form,
                action=url_for('summaries.update', id=id),
                submit_label='編集'
            )

    if form.errors:
        handle_form_errors(form)

    return render_template(
        'update.html',
        summary=summary,
        form=form,
        action=url_for('summaries.update', id=id),
        submit_label='編集'
    )

@summaries_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user_cognito_id = session.get('user_cognito_id')
    if not user_cognito_id:
        current_app.logger.error('❌ user_cognito_id 取得失敗（/delete）')
        flash('削除にはログインが必要です')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()
    if not summary:
        current_app.logger.critical(f'💥 user_cognito_id 不一致（/delete） - IP: {request.remote_addr}')
        flash('削除権限がありません')
        return redirect(url_for('main.main'))

    form = DeleteForm()
    form.id.data = summary.id

    if form.validate_on_submit():
        if int(form.id.data) != summary.id:
            current_app.logger.critical(f'💥 summary.id 不一致（/delete） - IP: {request.remote_addr}')
            flash('不正な削除リクエストです')
            return redirect(url_for('main.main'))

        try:
            db.session.delete(summary)
            db.session.commit()
            flash('データが削除されました')
            return redirect(url_for('summaries.index'))

        except Exception:
            db.session.rollback()
            current_app.logger.exception('❌ 削除エラー')
            flash('削除に失敗しました')
            return render_template('update.html',summary=summary, form=form)

    if form.errors:
        handle_form_errors(form)

    return redirect(url_for('summaries.index'))

@summaries_bp.route('/database_reset', methods=['POST'])
def reset_database_route():
    if database_reset():
        flash('初期状態に戻りました')
    else:
        flash('初期状態に戻りませんでした')
    return redirect(url_for('main.main'))

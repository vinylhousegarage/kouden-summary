import sys
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import SummaryForm, DeleteForm, CSRFForm
from app.models import Summary
from app.extensions import db
from app.utils.summaries_helpers import database_reset

summaries_bp = Blueprint('summaries', __name__)

@summaries_bp.route('/index')
def index():
    summaries = Summary.query.filter_by(user_cognito_id=session.get('user_cognito_id')).all()
    form = CSRFForm()
    return render_template('index.html', summaries=summaries, form=form)

@summaries_bp.route('/create', methods=['GET', 'POST'])
def create():
    print(f'🔹 `request` のスコープ確認: {request.method}', file=sys.stderr, flush=True)
    form = SummaryForm()

    print(f'🔹 request.form の中身: {request.form}', file=sys.stderr, flush=True)
    print(f'🔹 CSRF Token (form側): {form.csrf_token.data}', file=sys.stderr, flush=True)
    print(f"🔹 CSRF Token (request.form側): {request.form.get('csrf_token')}", file=sys.stderr, flush=True)

    print(f'🔹 `validate_on_submit()` の結果: {form.validate_on_submit()}', file=sys.stderr, flush=True)

    if not form.validate_on_submit():
        print(f'⚠️ `validate_on_submit()` が `False` です！', file=sys.stderr, flush=True)
        print(f'🔍 `validate()` の結果: {form.validate()}', file=sys.stderr, flush=True)
        if form.errors:
            print(f'❌ `form.errors`: {form.errors}', file=sys.stderr, flush=True)
        else:
            print(f'✅ `form.errors` は空（バリデーションには問題なし）', file=sys.stderr, flush=True)

    print(f'🔹 giver_name: {form.giver_name.data}', file=sys.stderr, flush=True)
    print(f'🔹 amount: {form.amount.data}', file=sys.stderr, flush=True)
    print(f'🔹 address: {form.address.data}', file=sys.stderr, flush=True)
    print(f'🔹 tel: {form.tel.data}', file=sys.stderr, flush=True)
    print(f'🔹 note: {form.note.data}', file=sys.stderr, flush=True)

    print(f'🔹 request.headers: {request.headers}', file=sys.stderr, flush=True)

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

            print(f'🔹 session の型: {type(session)}', file=sys.stderr, flush=True)
            print(f'🔹 session のキー一覧: {list(session.keys())}', file=sys.stderr, flush=True)
            for key, value in session.items():
                print(f'  🔹 {key}: {type(value)} = {value}', file=sys.stderr, flush=True)

            print('✅ 登録データ:', new_entry, file=sys.stderr, flush=True)

            db.session.add(new_entry)
            db.session.commit()

            flash('登録されました')

            print('🔄 リダイレクトを実行', file=sys.stderr, flush=True)
            return redirect(url_for('summaries.create'))

        except Exception as e:
            db.session.rollback()
            print(f'[❌登録エラー] {str(e)}', file=sys.stderr, flush=True)
            flash('登録に失敗しました')
            return render_template(
                'create.html',
                form=form,
                action=url_for('summaries.create'),
                submit_label='登録'
            )

    if form.errors:
        print(f'⚠️ バリデーションエラー発生！', file=sys.stderr, flush=True)
        print(f'🔍 `form.errors`: {form.errors}', file=sys.stderr, flush=True)
    else:
        print(f'✅ バリデーションエラーなし', file=sys.stderr, flush=True)

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
        flash('編集にはログインが必要です')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()

    if not summary:
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

        except Exception as e:
            db.session.rollback()
            print(f'[❌編集エラー] {str(e)}', file=sys.stderr, flush=True)
            flash('編集に失敗しました')
            return render_template(
                'update.html',
                summary=summary,
                form=form,
                action=url_for('summaries.update', id=id),
                submit_label='編集'
            )

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
        flash('削除にはログインが必要です')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()
    if not summary:
        flash('削除権限がありません')
        return redirect(url_for('main.main'))

    form = DeleteForm()
    form.id.data = summary.id
    print(f'✅ form.data: {form.data}', file=sys.stderr, flush=True)
    print(f'✅ form.errors: {form.errors}', file=sys.stderr, flush=True)
    print(f'📦 request.form: {request.form.to_dict()}', file=sys.stderr, flush=True)

    if form.validate_on_submit():
        if int(form.id.data) != summary.id:
            flash('不正な削除リクエストです')
            return redirect(url_for('main.main'))

        try:
            db.session.delete(summary)
            db.session.commit()
            flash('データが削除されました')
            return redirect(url_for('summaries.index'))
        except Exception as e:
            db.session.rollback()
            print(f'[❌削除エラー] {str(e)}', file=sys.stderr, flush=True)
            flash('削除に失敗しました')
            return render_template('update.html',summary=summary, form=form)

    flash('フォームの送信に失敗しました')
    return redirect(url_for('summaries.index'))

@summaries_bp.route('/database_reset', methods=['POST'])
def reset_database_route():
    if database_reset():
        flash('初期状態に戻りました')
    else:
        flash('初期状態に戻りませんでした')
    return redirect(url_for('main.main'))

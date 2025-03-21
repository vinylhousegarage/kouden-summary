import sys
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, session
from app.forms import SummaryForm
from app.forms import DeleteForm
from app.models import Summary
from app.extensions import db
from app.utils.summaries_helpers import database_reset

summaries_bp = Blueprint('summaries', __name__)

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

            flash('データが正常に作成されました！', 'success')

            print('🔄 リダイレクトを実行', file=sys.stderr, flush=True)
            return redirect(url_for('summaries.create'))

        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'danger')
            return render_template('create.html', form=form)

    if form.errors:
        print(f'⚠️ バリデーションエラー発生！', file=sys.stderr, flush=True)
        print(f'🔍 `form.errors`: {form.errors}', file=sys.stderr, flush=True)
    else:
        print(f'✅ バリデーションエラーなし', file=sys.stderr, flush=True)

    return render_template('create.html', form=form)

@summaries_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_cognito_id = session.get('user_cognito_id')
    if not user_cognito_id:
        flash('ログインが必要です。', 'warning')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()
    if not summary:
        flash('このデータにアクセスする権限がありません。', 'danger')
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

            flash('データが正常に更新されました！', 'success')
            return redirect(url_for('main.main'))

        except Exception as e:
            db.session.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'danger')
            return render_template('update.html', form=form)

    return render_template('update.html', form=form, summary=summary)

@summaries_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_cognito_id = session.get('user_cognito_id')
    if not user_cognito_id:
        flash('ログインが必要です。', 'warning')
        return redirect(url_for('auth.login'))

    summary = Summary.query.filter_by(id=id, user_cognito_id=user_cognito_id).first()
    if not summary:
        flash('このデータにアクセスする権限がありません。', 'danger')
        return redirect(url_for('main.main'))

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
        return jsonify({'message': '初期状態に戻りました'}), 200
    else:
        return jsonify({'error': '初期化に失敗しました'}), 500

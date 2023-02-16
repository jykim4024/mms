from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from src.models import db
from src.models.forms import UserLoginForm, UserCreateForm

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = db.select_userInfoById(form.usrId.data)
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user[0][3], form.passWord.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['usr_id'] = user[0][0]
            session['usr_nm'] = user[0][1]
            session['usr_typ_cd'] = user[0][2]
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    lnId = session.get('usr_id')

    if request.method == 'POST' and form.validate_on_submit():
        user = db.select_userInfoById(form.usrId.data)
        if not user:
            db.insert_userInfo(form.usrId.data, form.usrNm.data, form.usrtypcd.data,
                               generate_password_hash(form.pw1.data), form.gendercd.data, form.mobile.data,
                               form.emcmobile.data, form.email.data)
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    # dept_list = db.select_commCdList('DEPT_CD')
    # rank_list = db.select_commCdList('RANK_CD')
    return render_template('auth/signup.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user():
    usr_id = session.get('usr_id')
    if usr_id is None:
        g.user = None
    else:
        g.user = db.select_userInfoById(usr_id)

@bp.before_app_request
def user_auth():
    usr_id = session.get('usr_id')
    usr_typ = session.get('usr_typ_cd')
    if usr_id is None:
        g.auth = None
    else:
        g.auth = usr_typ
        if g.auth == '00':
            g.level = 'super'
        else:
            g.level = None

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         return view(**kwargs)
#     return wrapped_view
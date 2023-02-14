from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .. import db
from ..forms import UserCreateForm, UserLoginForm, UserModifyForm

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    lnId = session.get('user_id')

    if request.method == 'POST' and form.validate_on_submit():
        user = db.select_userInfoByName(form.username.data)
        if not user:
            bizNum = db.select_createBizNum()
            db.insert_userInfo(bizNum, form.username.data, generate_password_hash(form.password1.data), form.rankcd.data, form.deptcd.data, form.phonenum.data, form.hiredt.data, form.remark.data, lnId)
            if form.mnlyn.data == 'N':
              mnl_dnum = 0
              exhaust = 0.0
              leftover = 15.0
            else:
              mnl_dnum = form.mnldnum.data
              exhaust = 0.0
              leftover = form.mnldnum.data+'.0'
            db.insert_userVacInfo(bizNum, form.username.data, form.rankcd.data, form.deptcd.data, exhaust, leftover, form.mnlyn.data, mnl_dnum, lnId)
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    dept_list = db.select_commCdList('DEPT_CD')   
    rank_list = db.select_commCdList('RANK_CD') 
    return render_template('auth/signup.html', form=form, dept_list=dept_list, rank_list=rank_list)

@bp.route('/modify/<string:biznum>', methods=('GET', 'POST'))
def modify(biznum):
    form = UserModifyForm()
    lnId = session.get('user_id')
    user = db.select_userInfoById(biznum)
    if request.method == 'POST' and form.validate_on_submit():
      if g.level == 'super' or g.level == 'admin':
        db.update_userInfo(form.phonenum.data, form.rankcd.data, form.deptcd.data, form.remark.data, form.hiredt.data, form.email.data, biznum, lnId)  
      else:
        db.update_userInfo(form.phonenum.data, user[0][6], user[0][7], form.remark.data, user[0][2], form.email.data, biznum, lnId)
      if form.mnlyn.data == 'N':
        mnl_dnum = 0
        exhaust = 0.0
        leftover = 15.0
      else:
        mnl_dnum = form.mnldnum.data
        exhaust = 0.0
        leftover = form.mnldnum.data+'.0'
      db.update_userVacInfo(exhaust, leftover, form.mnlyn.data, mnl_dnum, lnId, biznum, 'g1')
      return redirect(url_for('main.index'))    
        
    dept_list = db.select_commCdList('DEPT_CD')   
    rank_list = db.select_commCdList('RANK_CD')
    my_vac_list = db.select_myVacList(biznum) 
    return render_template('auth/modify.html', form=form, user=user, dept_list=dept_list, rank_list=rank_list, my_vac_list=my_vac_list)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()  
    
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = db.select_userInfoById(form.biznum.data)  
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user[0][14], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user[0][0]
            session['level_cd'] = user[0][6]
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.select_userInfoById(user_id)

@bp.before_app_request
def user_auth():
    user_id = session.get('user_id')
    level_cd = session.get('level_cd')
    if user_id is None:
        g.auth = None
    else:
        g.auth = level_cd
        if g.auth == 'MD111' or g.auth == 'MD112':
            g.level = 'super'
        elif g.auth == 'MD119':
            g.level = 'admin'
        else:
            g.level = None

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
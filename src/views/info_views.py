from datetime import datetime

from flask import Blueprint, render_template, request, url_for, flash, session, g
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
from src.models import db
from src.models.forms import UserLoginForm

bp = Blueprint('userinfo', __name__, url_prefix='/userinfo')


@bp.route('/infolist/')
def infolist():
    usr_id = session.get('usr_id')
    info_list = db.select_userInfoById(usr_id)
    # if g.level == 'super' or g.level == 'admin':
    #     info_list = db.select_userInfoList('', 'super')
    # else:
    #     info_list = db.select_userInfoList(user_id, 'none')

    return render_template('userinfo/info.html', info_list=info_list)


# @bp.route('/change_pwd/', methods=('GET', 'POST'))
# def changepwd():
#     form = UserLoginForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         db.update_userPwd(generate_password_hash(form.password.data), session.get('user_id'))
#         return redirect(url_for('main.index'))
#     return render_template('userinfo/change_pwd.html', form=form)

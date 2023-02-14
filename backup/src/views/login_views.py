from flask import Blueprint, url_for, session, g
from werkzeug.utils import redirect

bp = Blueprint('login', __name__, url_prefix='/')

@bp.route('/')
def index():
    user_id = session.get('USR_ID')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('userinfo.infolist'))
        # return redirect(url_for('question._list'))
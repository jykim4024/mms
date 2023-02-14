from flask import Blueprint, url_for, session, g
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('userinfo.infolist'))
        # return redirect(url_for('question._list'))




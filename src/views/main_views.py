from flask import Blueprint, url_for, session, g
from werkzeug.utils import redirect

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def index():
    usr_id = session.get('usr_id')
    if usr_id is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('board.boardm'))
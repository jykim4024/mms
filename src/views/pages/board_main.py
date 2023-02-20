from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect

from src.models import db
from src.models.forms import BoardMstForm, BoardDtlForm

bp = Blueprint('board',__name__,url_prefix='/board')

@bp.route('/boardm/',methods=('GET','POST'))
def boardm():
    form = BoardMstForm()

    boardMainList = db.select_board_list()

    return render_template('pages/board_main.html', form=form, boardMainList=boardMainList)
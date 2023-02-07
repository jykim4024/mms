from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .. import db
from ..forms import UserVacForm
from datetime import datetime

bp = Blueprint('uservac', __name__, url_prefix='/uservac')

@bp.route('/vacinfo/', methods=('GET', 'POST'))
def vacinfo():
  form = UserVacForm()
  if request.method == 'POST' and form.validate_on_submit():
    now = datetime.now()
    str_now = now.strftime("%Y%m%d")
    if form.actiontype.data == 'SAVE':
      cnt = db.select_userVacInfoExists(form.biznum.data, form.vacdt.data)
      if cnt[0][0] > 0:
        flash(form.vacdt.data+'일 휴가가 존재합니다.')
      else:      
        db.update_userVacInfo(form.exhaust.data, form.leftover.data, form.mnlyn.data, form.mnldnum.data, session.get('user_id'), form.biznum.data, 'g1')
        db.insert_userVacHistInfo(session.get('user_id'), form.vacdt.data, str_now, form.vacty.data, form.vacapty.data, form.prosts.data, form.vacsts.data, form.remark.data, session.get('user_id'))
    elif form.actiontype.data == 'MODIFY':
      db.update_userVacInfo(form.exhaust.data, form.leftover.data, form.mnlyn.data, form.mnldnum.data, session.get('user_id'), form.biznum.data, 'g1')
      db.delete_userVacHistInfo(form.biznum.data, form.prevacdt.data)
      db.insert_userVacHistInfo(session.get('user_id'), form.vacdt.data, str_now, form.vacty.data, form.vacapty.data, form.prosts.data, form.vacsts.data, form.remark.data, session.get('user_id'))
    elif form.actiontype.data == 'CANCEL':
      db.update_userVacInfo(form.exhaust.data, form.leftover.data, form.mnlyn.data, form.mnldnum.data, session.get('user_id'), form.biznum.data, 'g1')
      db.delete_userVacHistInfo(form.biznum.data, form.vacdt.data)
    elif form.actiontype.data == 'AGREE':
      db.update_userVacHistInfo(form.prosts.data, session.get('user_id'), form.biznum.data, form.vacdt.data)
    elif form.actiontype.data == 'DENY':
      #db.update_userVacInfo(form.exhaust.data, form.leftover.data, '', '', session.get('user_id'), form.biznum.data, 'g2')
      db.update_userVacHistInfo(form.prosts.data, session.get('user_id'), form.biznum.data, form.vacdt.data)


  user = db.select_userInfoById(session.get('user_id'))
  my_vac_list = db.select_myVacList(session.get('user_id'))
  vac_req_list = db.select_vacReqList()

  vac_ty = db.select_commCdList('M0004')
  vac_ap_ty = db.select_commCdList('M0005')
  vac_sts = db.select_commCdList('M0009')
  return render_template('uservac/vacinfo.html', form=form, my_vac_list=my_vac_list, user=user, vac_ty=vac_ty, vac_ap_ty=vac_ap_ty, vac_sts=vac_sts, vac_req_list=vac_req_list)

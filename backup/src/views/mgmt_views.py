from flask import Blueprint, url_for, render_template, flash, request, session, jsonify

from .. import db
from ..forms import mgmtSrchForm, mgmtDetailForm
from datetime import datetime

bp = Blueprint('mgmt', __name__, url_prefix='/mgmt')

@bp.route('/mgmtinfo/', methods=('GET', 'POST'))
def mgmtinfo():
  form = mgmtSrchForm()
  if request.method == 'GET':
    mstcd = request.args.get('mstcd', type=str, default='ALL')
    detcd = request.args.get('detcd', type=str, default='ALL')
    stdt = request.args.get('stdt', type=str, default='')
    eddt = request.args.get('eddt', type=str, default='')
    useyn = request.args.get('useyn', type=str, default='Y')

  gubun = 'ALL'
  if(mstcd != 'ALL'):
    gubun = 'MST'

  if(mstcd != 'ALL' and detcd != '1'):
    gubun = 'DET'

  mgmt_list = db.select_mgmtList(stdt, eddt, useyn, mstcd, detcd, gubun)

  mst_cd = db.select_commCdMgmtList()
  return render_template('mgmt/mgmtinfo.html', form=form, mgmt_list=mgmt_list, mst_cd=mst_cd, mstcd=mstcd, detcd=detcd)

@bp.route('/mgmtinfo/get_items', methods=['POST']) 
def add_items(): 
  mst_cd = request.form['mst_cd']  
  det_cd = db.select_commCdList(mst_cd)
  return jsonify(det_cd)

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    form = mgmtDetailForm()

    if request.method == 'POST' and form.validate_on_submit():
      now = datetime.now()
      str_now = now.strftime("%Y%m%d")
      seriallist = request.values.getlist('serialnum')
      datatx1list = request.values.getlist('datatx1')
      datatx2list = request.values.getlist('datatx2')
      for i in range(len(seriallist)):
        if(seriallist[i] != ''):
          db.insert_mgmtdata(str_now, form.mstcd.data, form.detcd.data, datatx1list[i], datatx2list[i], seriallist[i])

    mst_cd = db.select_commCdMgmtList()
    return render_template('mgmt/register.html', form=form, mst_cd=mst_cd)

@bp.route('/mgmtdetail/<string:mgmtnum>', methods=('GET', 'POST'))
def mgmtdetail(mgmtnum):
    form = mgmtDetailForm()

    if request.method == 'POST' and form.validate_on_submit():
      db.update_mgmtInfo(form.datatx1.data, form.datatx2.data, form.datatx3.data, form.datanum1.data, form.datanum2.data, form.datanum3.data, form.useyn.data, session.get('user_id'), form.mgmtnum.data)

      
    detail = db.select_mgmtInfo(mgmtnum)
    return render_template('mgmt/detail.html', form=form, detail=detail, mgmtnum=mgmtnum)
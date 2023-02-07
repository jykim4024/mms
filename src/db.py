from .modules import collection as clt

config = clt.configparser.ConfigParser()
# config.read('../config/config.ini')

# host = config['MariaDB']['HOST']
# port = config['MariaDB']['PORT']
# database = config['MariaDB']['DB']
# username = config['MariaDB']['USERNAME']
# password = config['MariaDB']['PASSWORD']

def db_conn():
    # conn = clt.db.connect(host=host, user=username, password=password, db=database, charset='utf8', port=int(port))
    conn = clt.db.connect(host='192.168.0.250', user='nexcore', password='nexcore0309!', db='nexcore_nms', charset='utf8', port=3306)
    return conn

# 사번으로 사용자정보 조회
def select_userInfoById(userId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select a.biz_num, a.emp_nm, a.hire_dt, b.mnl_yn, b.mnl_dnum, a.phone_num, a.rank_cd, a.dept_cd, a.email, a.remark, comm_getNm('RANK_CD',a.rank_cd), comm_getNm('DEPT_CD',a.dept_cd), b.exhaust, b.leftover, a.pwd from nx_emp a left join nx_vac b on a.biz_num = b.biz_num where a.biz_num = %s limit 1"            
            curs.execute(sql,(userId))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 이름으로 사용자정보 조회
def select_userInfoByName(userNm):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select biz_num, emp_nm, rank_cd, dept_cd, pwd from nx_emp where emp_nm = %s limit 1"
            curs.execute(sql,(userNm))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 비밀번호 조회
def select_userPassword(biznum, password):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select biz_num, emp_nm, rank_cd, dept_cd from nx_emp where biz_num = %s and pwd = %s limit 1"
            curs.execute(sql,(biznum, password))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 사용자 목록조회
def select_userInfoList(biznum, gubun):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            if gubun == 'super':
              sql = "select a.biz_num, a.emp_nm" \
                    ", a.hire_dt, b.mnl_yn, b.mnl_dnum, b.exhaust, b.leftover, comm_getNm('RANK_CD',a.rank_cd) as rank, comm_getNm('DEPT_CD',a.dept_cd) as dept " \
                    "from nx_emp a left outer join nx_vac b on a.biz_num = b.biz_num order by a.rank_cd, a.emp_nm, a.biz_num"
              curs.execute(sql)
            elif gubun == 'none':
              sql = "select a.biz_num, a.emp_nm" \
                    ", a.hire_dt, b.mnl_yn, b.mnl_dnum, b.exhaust, b.leftover, comm_getNm('RANK_CD',a.rank_cd) as rank, comm_getNm('DEPT_CD',a.dept_cd) as dept " \
                    "from nx_emp a left outer join nx_vac b on a.biz_num = b.biz_num where a.biz_num = %s"
              curs.execute(sql,(biznum))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 일별 휴가 현황
def select_dailyVacList():
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = " select a.biz_num, a.emp_nm, date_format(STR_TO_DATE(b.vac_dt, '%Y%m%d'),'%Y-%m-%d'), comm_getNm('M0004',b.vac_ty), comm_getNm('M0005',b.vac_ap_ty), "\
            " comm_getNm('M0006',b.pro_sts), comm_getNm('M0009',b.vac_sts), b.remark, case when b.vac_dt = date_format(now(), '%Y%m%d') then 'Y' else 'N' end as vac_now_chk " \
            "from nx_emp a left join nx_vac_hist b on a.biz_num = b.biz_num where b.pro_sts = 'MD602' "\
            " and b.vac_dt between date_format(now(), '%Y%m%d') and date_format((date_add(now(), interval 14 day)),'%Y%m%d') " \
            " order by b.vac_dt, a.biz_num"
            curs.execute(sql)
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 나의 휴가현황
def select_myVacList(biznum):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = " select date_format(STR_TO_DATE(vac_dt, '%%Y%%m%%d'),'%%Y-%%m-%%d'), date_format(STR_TO_DATE(req_dt, '%%Y%%m%%d'),'%%Y-%%m-%%d'), vac_ty, comm_getNm('M0004',vac_ty),"\
            " vac_ap_ty, comm_getNm('M0005',vac_ap_ty), pro_sts, comm_getNm('M0006',pro_sts), vac_sts, comm_getNm('M0009',vac_sts), remark, "\
            " case when vac_dt < date_format(now(), '%%Y%%m%%d') then 'Y' else 'N' end as vac_past, case when vac_dt = date_format(now(), '%%Y%%m%%d') then 'Y' else 'N' end as vac_now_chk "\
            " from nx_vac_hist where biz_num = %s order by vac_dt"
            curs.execute(sql,(biznum))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 휴가요청 목록조회
def select_vacReqList():
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = " select a.biz_num, a.emp_nm, date_format(STR_TO_DATE(b.vac_dt, '%Y%m%d'),'%Y-%m-%d'), comm_getNm('M0004',b.vac_ty), comm_getNm('M0005',b.vac_ap_ty), "\
            " comm_getNm('M0006',b.pro_sts), comm_getNm('M0009',b.vac_sts), b.remark, b.vac_ty, b.vac_ap_ty, b.vac_sts, c.exhaust, c.leftover "\
            " from nx_emp a left join nx_vac_hist b on a.biz_num = b.biz_num left join nx_vac c on a.biz_num = c.biz_num where b.pro_sts = 'MD601' "\
            " order by a.biz_num, b.vac_dt "
            curs.execute(sql)
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 사번 생성
def select_createBizNum():
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select concat('NX', lpad((select max(substr(x.biz_num,3,6)) +1 from nx_emp x),4,0))  from dual"
            curs.execute(sql)
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 사용자정보 저장
def insert_userInfo(bizNum, empNm, pwd, rankCd, deptCd, phoneNum, hireDt, remark, lnId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "insert into nx_emp (biz_num, emp_nm, pwd, rank_cd, dept_cd, phone_num, hire_dt, remark, mod_id, mod_dtm)"\
                  " values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
            curs.execute(sql, (bizNum, empNm, pwd, rankCd, deptCd, phoneNum, hireDt, remark, lnId))
        conn.commit()
    finally:
        conn.close()

# 사용자정보 수정
def update_userInfo(phonenum, rankcd, deptcd, remark, hiredt, email, bizmum, lnid):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "update nx_emp set phone_num = %s, rank_cd = %s, dept_cd = %s, remark = %s, hire_dt = %s, email = %s, mod_id = %s, mod_dtm = now() where biz_num = %s"
            curs.execute(sql, (phonenum, rankcd, deptcd, remark, hiredt, email, lnid, bizmum))
        conn.commit()
    finally:
        conn.close()

# 휴가정보 저장
def insert_userVacInfo(bizNum, empNm, rankcd, deptcd, exhaust, leftover, mnlyn, mnldnum, lnId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "insert into nx_vac (biz_num, emp_nm, rank_cd, dept_cd, exhaust, leftover, mnl_yn, mnl_dnum, mod_id, mod_dtm)"\
                  " values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
            curs.execute(sql, (bizNum, empNm, rankcd, deptcd, exhaust, leftover, mnlyn, mnldnum, lnId))
        conn.commit()
    finally:
        conn.close()

# 휴가정보 수정
def update_userVacInfo(exhaust, leftover, mnlyn, mnldnum, lnId, bizNum, gubun):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
          if gubun == 'g1':
            sql = "update nx_vac set exhaust = %s, leftover = %s, mnl_yn = %s, mnl_dnum = %s, mod_id = %s, mod_dtm = now() where biz_num = %s"
            curs.execute(sql, (exhaust, leftover, mnlyn, mnldnum, lnId, bizNum))
          elif gubun == 'g2':
            sql = "update nx_vac set exhaust = %s, leftover = %s, mod_id = %s, mod_dtm = now() where biz_num = %s"
            curs.execute(sql, (exhaust, leftover, lnId, bizNum))
        conn.commit()
    finally:
        conn.close()

# 휴가 중복 조회
def select_userVacInfoExists(biznum, vacdt):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select count(*)from nx_vac_hist where biz_num = %s and vac_dt = replace(%s,'-','') and pro_sts in ('MD601', 'MD602')"
            curs.execute(sql,(biznum, vacdt))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 휴가이력정보 저장
def insert_userVacHistInfo(bizNum, vacdt, reqdt, vacty, vacapty, prosts, vacsts, remark, lnId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "insert into nx_vac_hist (biz_num, vac_dt, req_dt, vac_ty, vac_ap_ty, pro_sts, vac_sts, remark, mod_id, mod_dtm)"\
                  " values(%s, replace(%s,'-',''), %s, %s, %s, %s, %s, %s, %s, now())"
            curs.execute(sql, (bizNum, vacdt, reqdt, vacty, vacapty, prosts, vacsts, remark, lnId))
        conn.commit()
    finally:
        conn.close()

# 휴가이력정보 수정
def update_userVacHistInfo(prosts, lnId, bizNum, vacdt):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "update nx_vac_hist set pro_sts = %s, mod_id = %s, mod_dtm = now() where biz_num = %s and vac_dt = replace(%s,'-','')"
            curs.execute(sql, (prosts, lnId, bizNum, vacdt))
        conn.commit()
    finally:
        conn.close()

# 휴가이력정보 삭제
def delete_userVacHistInfo(bizNum, vacdt):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "delete from nx_vac_hist where biz_num = %s and vac_dt = replace(%s,'-','')"
            curs.execute(sql, (bizNum, vacdt))
        conn.commit()
    finally:
        conn.close()

# 재고관리 목록조회
def select_mgmtList(stdt, eddt, useyn, mstcd, detcd, gubun):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            if(gubun == 'ALL'):
              sql = " select a.mgmt_num, a.strd_dt, a.mst_cd, b.mst_nm, a.det_cd, b.det_nm, a.data_tx_1, a.data_tx_2, a.data_tx_3,  "\
              " a.data_num_1, a.data_num_2, a.data_num_3, a.serial_num, a.use_yn "\
              " from nx_mgmt_spc a join nx_comm b on a.mst_cd = b.mst_cd and a.det_cd = b.det_cd  and a.strd_dt between replace(%s,'-','') and replace(%s,'-','') "\
              " and a.use_yn = %s"
              " order by a.mgmt_num"
            elif(gubun =='MST'):
              sql = " select a.mgmt_num, a.strd_dt, a.mst_cd, b.mst_nm, a.det_cd, b.det_nm, a.data_tx_1, a.data_tx_2, a.data_tx_3,  "\
              " a.data_num_1, a.data_num_2, a.data_num_3, a.serial_num, a.use_yn "\
              " from nx_mgmt_spc a join nx_comm b on a.mst_cd = b.mst_cd and a.det_cd = b.det_cd  and a.strd_dt between replace(%s,'-','') and replace(%s,'-','') "\
              " and a.use_yn = %s and a.mst_cd = %s"
              " order by a.mgmt_num"
            elif(gubun == 'DET'):
              sql = " select a.mgmt_num, a.strd_dt, a.mst_cd, b.mst_nm, a.det_cd, b.det_nm, a.data_tx_1, a.data_tx_2, a.data_tx_3,  "\
              " a.data_num_1, a.data_num_2, a.data_num_3, a.serial_num, a.use_yn "\
              " from nx_mgmt_spc a join nx_comm b on a.mst_cd = b.mst_cd and a.det_cd = b.det_cd  and a.strd_dt between replace(%s,'-','') and replace(%s,'-','') "\
              " and a.use_yn = %s and a.mst_cd = %s and a.det_cd = %s"
              " order by a.mgmt_num"
            if(gubun == 'ALL'):            
              curs.execute(sql,(stdt, eddt, useyn))
            elif(gubun =='MST'):
              curs.execute(sql,(stdt, eddt, useyn, mstcd))
            elif(gubun == 'DET'):
              curs.execute(sql,(stdt, eddt, useyn, mstcd, detcd))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 재고관리 등록
def insert_mgmtdata(strdDt,mstCd,detCd,data1,data2,serial):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "INSERT INTO nx_mgmt_spc (mgmt_num, strd_dt, mst_cd, det_cd, data_tx_1, data_tx_2, data_tx_3,data_num_1,data_num_2,data_num_3, serial_num, use_yn, mod_id, mod_dtm)" \
                  "VALUES(nextval(sq_mgmt_num), %s, %s, %s, %s, %s,'-',0,0,0,%s,'Y', 'system', sysdate())"
            curs.execute(sql,(strdDt,mstCd,detCd,data1,data2,serial))
            conn.commit()
    finally:
        conn.close()

# 재고관리 상세조회
def select_mgmtInfo(mgmtnum):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = " select a.mgmt_num, a.strd_dt, a.mst_cd, b.mst_nm, a.det_cd, b.det_nm, a.data_tx_1, a.data_tx_2, a.data_tx_3,  "\
            " a.data_num_1, a.data_num_2, a.data_num_3, a.serial_num, a.use_yn "\
            " from nx_mgmt_spc a join nx_comm b on a.mst_cd = b.mst_cd and a.det_cd = b.det_cd "\
            " and a.mgmt_num = %s"
            " order by a.mgmt_num"
            curs.execute(sql,(mgmtnum))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 재고관리 수정
def update_mgmtInfo(datatx1, datatx2, datatx3, datanum1, datanum2, datanum3, useyn, lnId, mgmtnum):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "update nx_mgmt_spc set data_tx_1 = %s, data_tx_2 = %s, data_tx_3 = %s, "\
                  " data_num_1 = %s, data_num_2 = %s, data_num_3 = %s, use_yn = %s, mod_id = %s, mod_dtm = now() where mgmt_num = %s "
            curs.execute(sql, (datatx1, datatx2, datatx3, datanum1, datanum2, datanum3, useyn, lnId, mgmtnum))
        conn.commit()
    finally:
        conn.close()

# 공통코드 조회
def select_commCdList(commCd):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select det_cd, det_nm from nx_comm where mst_cd = %s order by sort_order "
            curs.execute(sql,(commCd))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 재고관리 대분류 조회
def select_commCdMgmtList():
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "select 'ALL', 'ALL' from dual union all select distinct(mst_cd), mst_nm from nx_comm where mst_cd like 'D0%'"
            curs.execute(sql)
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

# 비밀번호 수정
def update_userPwd(password, bizNum):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "update nx_emp set pwd = %s where biz_num = %s"
            curs.execute(sql, (password, bizNum))
        conn.commit()
    finally:
        conn.close()
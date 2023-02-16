from src.modules import collection as clt

config = clt.configparser.ConfigParser()

def db_conn():
    conn = clt.db.connect(host='3.39.96.245', user='dev01', password='juny6521!!', db='ADB', charset='utf8', port=3306)
    return conn

def select_userInfoById(usrId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "SELECT UM.USR_ID , UM.USR_NM , UM.USR_TYP_CD , CONCAT('pbkdf2:sha256:',UM.PW) , UM.GENDER_CD , UM.MOBILE , UM.EMC_MOBILE , UM.EMAIL FROM USER_MST AS UM WHERE UM.USR_ID = %s"
            curs.execute(sql, (usrId))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()

def insert_userInfo(usrId,usrNm,usrTypCd,pw,genderCd,mobile,emcMobile,email):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "INSERT INTO USER_MST (USR_ID,USR_NM,USR_TYP_CD,PW,GENDER_CD,MOBILE,EMC_MOBILE,EMAIL,REG_DTM,REG_USR_ID,UPD_DTM,UPD_USR_ID)" \
                  "VALUES (%s,%s,%s,SUBSTRING_INDEX(%s,':',-1),%s,TRIM(REPLACE(REPLACE(%s,'-',''),' ','')),TRIM(REPLACE(REPLACE(%s,'-',''),' ','')),%s,NOW(),'system',NOW(),'system')"
            curs.execute(sql,(usrId,usrNm,usrTypCd,pw,genderCd,mobile,emcMobile,email))
            conn.commit()
    finally:
        conn.close()

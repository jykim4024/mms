from .modules import collection as clt

config = clt.configparser.ConfigParser()

def db_conn():
    conn = clt.db.connect(host='3.39.96.245', user='dev01', password='juny6521!!', db='ADB', charset='utf8', port=3306)
    return conn

def select_userInfoById(usrId):
    conn = db_conn()
    try:
        with conn.cursor() as curs:
            sql = "SELECT UM.USR_ID , UM.USR_NM , UM.USR_TYP_CD , UM.PW , UM.GENDER_CD , UM.MOBILE , UM.EMC_MOBILE , UM.EMAIL FROM USER_MST AS UM WHERE UM.USR_ID = %s"
            curs.execute(sql, (usrId))
            rs = curs.fetchall()
            return rs
    finally:
        conn.close()
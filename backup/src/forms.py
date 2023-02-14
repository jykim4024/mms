from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = StringField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = StringField('비밀번호확인', validators=[DataRequired()])
    phonenum = StringField('전화번호', validators=[DataRequired(), Length(min=6, max=20)])
    rankcd = StringField('직급코드', validators=[DataRequired()])
    deptcd = StringField('부서코드', validators=[DataRequired()])
    hiredt = StringField('입사일자')
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    mnlyn = StringField('수동할당여부', validators=[DataRequired()])
    mnldnum = StringField('수동할당일자', validators=[DataRequired()])
    remark = StringField('비고')

class UserModifyForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    phonenum = StringField('전화번호', validators=[DataRequired(), Length(min=6, max=20)])
    rankcd = StringField('직급코드', validators=[DataRequired()])
    deptcd = StringField('부서코드', validators=[DataRequired()])
    hiredt = StringField('입사일자')
    email = EmailField('이메일', validators=[Email()])
    mnlyn = StringField('수동할당여부', validators=[DataRequired()])
    mnldnum = StringField('수동할당일자', validators=[DataRequired()])
    remark = StringField('비고')

class UserVacForm(FlaskForm):
    biznum = StringField('사번')
    vacdt = StringField('휴가일자', validators=[DataRequired()])
    reqdt = StringField('요청일자')
    vacty = StringField('휴가종류', validators=[DataRequired()])   
    vacapty = StringField('휴가신청유형', validators=[DataRequired()])
    prosts = StringField('진행상태') 
    vacsts = StringField('휴가상태', validators=[DataRequired()])
    exhaust = StringField('휴가소진일수')
    leftover = StringField('잔여휴가일수')
    mnlyn = StringField('수동할당여부')
    mnldnum = StringField('수동할당일자')
    remark = StringField('비고')
    actiontype = StringField('화면수행종류')
    vacdtchangeyn = StringField('휴가일변경여부')
    prevacdt = StringField('기존휴가일자')
    prevacty = StringField('기존휴가종류')
    prevacapty = StringField('기존신청유형')
    prevacsts = StringField('기존휴가상태')
    preremark = StringField('기존비고')

class UserLoginForm(FlaskForm):
    biznum = StringField('사번', validators=[DataRequired(), Length(min=3, max=25)])
    password = StringField('비밀번호', validators=[DataRequired()])

class mgmtSrchForm(FlaskForm):
  mstcd = StringField('마스터코드')
  detcd = StringField('상세코드')
  stdt = StringField('기준시작일')
  eddt = StringField('기준종료일')
  useyn = StringField('사용여부')

class mgmtDetailForm(FlaskForm):
  mgmtnum = StringField('관리번호')  
  strddt = StringField('기준일자')
  mstcd = StringField('마스터코드')
  detcd = StringField('상세코드')
  datatx1 = StringField('데이터텍스트1')
  datatx2 = StringField('데이터텍스트2')
  datatx3 = StringField('데이터텍스트3')
  datanum1 = IntegerField('데이터숫자1')
  datanum2 = IntegerField('데이터숫자2')
  datanum3 = IntegerField('데이터숫자3')
  serialnum = StringField('일련번호')
  useyn = StringField('사용여부')
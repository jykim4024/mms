from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserLoginForm(FlaskForm):
    usrId = StringField('로그인ID',validators=[DataRequired(), Length(min=3, max=20)])
    passWord = StringField('비밀번호',validators=[DataRequired()])

class UserCreateForm(FlaskForm):
    usrNm = StringField('사용자명', validators=[DataRequired(), Length(min=3, max=100)])
    pw1 = StringField('비밀번호', validators=[DataRequired(), EqualTo('pw2', '비밀번호가 일치하지 않습니다')])
    pw2 = StringField('비밀번호확인', validators=[DataRequired()])
    mobile = StringField('핸드폰번호', validators=[DataRequired(), Length(min=3, max=20)])
    emcmobile = StringField('비상연락핸드폰번호', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    gendercd = StringField('성별코드', validators=[DataRequired(), Length(min=3, max=20)])
    usrtypcd = StringField('사용자유형코드', validators=[DataRequired(), Length(min=3, max=20)])
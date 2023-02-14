# from . import db

# question_voter = db.Table(
#     'question_voter',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
#     db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
# )

# answer_voter = db.Table(
#     'answer_voter',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
#     db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
# )

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     subject = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     user = db.relationship('User', backref=db.backref('question_set'))
#     modify_date = db.Column(db.DateTime(), nullable=True)
#     voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
#     question = db.relationship('Question', backref=db.backref('answer_set'))
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     user = db.relationship('User', backref=db.backref('answer_set'))
#     modify_date = db.Column(db.DateTime(), nullable=True)
#     voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     biznum = db.Column(db.String(100), unique=False, nullable=True)
#     rankcd = db.Column(db.String(10), unique=False, nullable=True)
#     deptcd = db.Column(db.String(10), unique=False, nullable=True)
#     phonenum = db.Column(db.String(100), unique=False, nullable=True)
#     hidt = db.Column(db.String(10), unique=False, nullable=True)
#     redt = db.Column(db.String(10), unique=False, nullable=True)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     user = db.relationship('User', backref=db.backref('comment_set'))
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     modify_date = db.Column(db.DateTime())
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
#     question = db.relationship('Question', backref=db.backref('comment_set'))
#     answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
#     answer = db.relationship('Answer', backref=db.backref('comment_set'))

# class Vac(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     biznum = db.Column(db.String(100), unique=False, nullable=True)
#     mnlyn = db.Column(db.String(10), unique=False, nullable=True)
#     mnl_dnum = db.Column(db.Integer, nullable=True)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     modify_date = db.Column(db.DateTime(), nullable=True)

# class Vachist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     biznum = db.Column(db.String(100), unique=False, nullable=True)
#     vacdt = db.Column(db.String(20), unique=False, nullable=True)
#     req_dt = db.Column(db.String(20), unique=False, nullable=True)
#     vac_ty = db.Column(db.String(10), unique=False, nullable=True)
#     vac_ap_ty = db.Column(db.String(10), unique=False, nullable=True)
#     pro_sts = db.Column(db.String(10), unique=False, nullable=True)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     modify_date = db.Column(db.DateTime(), nullable=True)
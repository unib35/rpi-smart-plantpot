from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 주소를 입력해주세요.')
    ])
    
    password = PasswordField('비밀번호', validators=[
        DataRequired(),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.'),
        Regexp(r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&^#])[a-z\d@$!%*?&^#]{6,}$',
               message='비밀번호는 소문자, 숫자 및 특수 문자를 포함해야 합니다.')
    ])
    
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('회원가입')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('이미 사용중인 사용자 이름입니다.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 등록된 이메일입니다.')

class LoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class FindIDForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 주소를 입력해주세요.')
    ])
    submit = SubmitField('아이디 찾기')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 주소를 입력해주세요.')
    ])
    submit = SubmitField('비밀번호 재설정 링크 받기')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('새 비밀번호', validators=[
        DataRequired(),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.'),
        Regexp(r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&^#])[a-z\d@$!%*?&^#]{6,}$',
               message='비밀번호는 소문자, 숫자 및 특수 문자를 포함해야 합니다.')
    ])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('비밀번호 재설정')

class EmailVerificationForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 주소를 입력해주세요.')
    ])
    submit = SubmitField('인증 요청')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('현재 비밀번호', validators=[DataRequired()])
    new_password = PasswordField('새 비밀번호', validators=[
        DataRequired(),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    
    confirm_new_password = PasswordField('새 비밀번호 확인', validators=[
        DataRequired(),
        EqualTo('new_password', message='새 비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('비밀번호 변경')

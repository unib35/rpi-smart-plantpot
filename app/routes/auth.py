from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.forms import (RegistrationForm, LoginForm, FindIDForm, 
                      ResetPasswordRequestForm, ResetPasswordForm, 
                      ChangePasswordForm)
from flask_mail import Message
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('로그인 실패. 다시 시도하세요.')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/find_id', methods=['GET', 'POST'])
def find_id():
    form = FindIDForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(f'회원님의 아이디는 {user.username} 입니다.', 'success')
        else:
            flash('해당 이메일로 등록된 사용자가 없습니다.', 'error')
        return redirect(url_for('auth.find_id'))
    
    return render_template('find_id.html', form=form)

def send_password_reset_email(user):
    token = generate_reset_token(user.email)
    msg = Message('비밀번호 재설정 요청',
                  recipients=[user.email])
    
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg.body = f'''비밀번호를 재설정하려면 다음 링크를 클릭하세요:
{reset_url}

이 링크는 1시간 동안만 유효합니다.

본인이 요청하지 않았다면 이 메일을 무시하세요.
'''
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"이메일 전송 오류: {str(e)}")
        return False

def generate_reset_token(email):
    exp_time = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(
        {
            'email': email,
            'exp': exp_time
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def verify_reset_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return User.query.filter_by(email=data['email']).first()
    except:
        return None

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if send_password_reset_email(user):
                flash('비밀번호 재설정 링크가 이메일로 전송되었습니다.')
                return redirect(url_for('auth.login'))
            else:
                flash('이메일 전송 중 오류가 발생했습니다. 나중에 다시 시도해주세요.')
        else:
            flash('해당 이메일로 등록된 계정을 찾을 수 없습니다.')
    
    return render_template('reset_password_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = verify_reset_token(token)
    if not user:
        flash('유효하지 않거나 만료된 토큰입니다.')
        return redirect(url_for('auth.reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('비밀번호가 재설정되었습니다.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form)

@auth_bp.route('/check_username', methods=['POST'])
def check_username():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return {'exists': user is not None}

@auth_bp.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return {'exists': user is not None}

@auth_bp.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html')

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('비밀번호가 변경되었습니다.')
            return redirect(url_for('auth.mypage'))
        else:
            flash('현재 비밀번호가 일치하지 않습니다.')
    return render_template('change_password.html', form=form)

@auth_bp.route('/delete_account')
@login_required
def delete_account():
    user = current_user
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('회원 탈퇴가 완료되었습니다.')
    return redirect(url_for('main.index'))

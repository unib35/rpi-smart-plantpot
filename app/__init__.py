from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from app.extensions import db, login_manager
from app.config import Config
from .models import User, ChatHistory

mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # 블루프린트 등록
    from app.routes import auth_bp, main_bp, video_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)
    
    # 모델 import
    from app import models
    
    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()
        
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app
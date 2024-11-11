import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    # 기본 설정
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Flask 설정
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'tamagotchi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 메일 설정
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    # OpenAI API 설정
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(Config.basedir, 'instance', 'tamagotchi_dev.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'instance', 'tamagotchi_test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


# 환경 설정 딕셔너리
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

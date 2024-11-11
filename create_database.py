from app import create_app, db
from models import User  # User 모델을 가져옵니다.

app = create_app()

# 애플리케이션 컨텍스트 내에서 데이터베이스 초기화
with app.app_context():
    print("Starting to create tables...")
    try:
        db.create_all()  # 모든 모델에 대한 테이블 생성
        print("Database initialized with users table.")
    except Exception as e:
        print(f"An error occurred: {e}")

import os

# 24바이트의 랜덤 비밀 키 생성
secret_key = os.urandom(24).hex()
print(secret_key)  # 생성된 비밀 키를 출력합니다.

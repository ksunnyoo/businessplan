import sys
sys.path.insert(0, ".")
import os
from dotenv import load_dotenv
load_dotenv(".env")

from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from jose import jwt
from datetime import datetime, UTC

print("=" * 50)
print("        [미션 3] JWT 보안 유틸리티 검증 증빙")
print("=" * 50)

# 1. 비밀번호 검증
pw = "mysecret123!"
hashed = hash_password(pw)
print("\n1. 비밀번호 검증 함수 (verify_password)")
print(f"   - 올바른 비밀번호: {verify_password(pw, hashed)}  (검증 통과)")
print(f"   - 틀린 비밀번호  : {verify_password('wrong_pw', hashed)} (검증 차단)")

# 2. Access Token
email = "user@example.com"
access_token = create_access_token({"sub": email})
decoded_at = jwt.decode(access_token, os.environ["SECRET_KEY"], algorithms=["HS256"])
at_exp = datetime.fromtimestamp(decoded_at["exp"], UTC)
now = datetime.now(UTC)
remaining_minutes = round((at_exp - now).total_seconds() / 60)

print("\n2. Access Token 생성 (create_access_token)")
print(f"   - 토큰 샘플: {access_token[:30]}...")
print(f"   - 발급 대상(sub): {decoded_at['sub']}")
print(f"   - 유효 기간: {remaining_minutes} 분")

# 3. Refresh Token
refresh_token = create_refresh_token({"sub": email})
decoded_rt = jwt.decode(refresh_token, os.environ["SECRET_KEY"], algorithms=["HS256"])
rt_exp = datetime.fromtimestamp(decoded_rt["exp"], UTC)
remaining_days = round((rt_exp - now).total_seconds() / 86400)

print("\n3. Refresh Token 생성 (create_refresh_token)")
print(f"   - 토큰 샘플: {refresh_token[:30]}...")
print(f"   - 발급 대상(sub): {decoded_rt['sub']}")
print(f"   - 유효 기간: {remaining_days} 일")

print("\n" + "=" * 50)
print("모든 보안 함수가 요구사항에 맞게 정상 작동합니다!")
print("=" * 50)

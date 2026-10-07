# ───────────────────────────────────────────────────────────
# JWT 보안 유틸리티
# - verify_password : bcrypt 비밀번호 검증
# - hash_password   : bcrypt 비밀번호 해시 생성
# - create_access_token  : 단기 API 신분증 (30분)
# - create_refresh_token : 장기 재발급 티켓 (7일)
# ───────────────────────────────────────────────────────────

import os
from datetime import UTC, datetime, timedelta

import bcrypt
from dotenv import load_dotenv
from jose import jwt

load_dotenv()

SECRET_KEY: str = os.environ["SECRET_KEY"]
ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


# ── 비밀번호 해시 생성 ─────────────────────────────────────
def hash_password(plain_password: str) -> str:
    """평문 비밀번호를 bcrypt 알고리즘으로 해시화하여 반환합니다."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# ── 비밀번호 검증 ─────────────────────────────────────────
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """로그인 시 입력한 평문과 DB의 해시 비밀번호 일치 여부를 확인합니다."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ── JWT 토큰 생성 공통 함수 ───────────────────────────────
def _create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ── Access Token 생성 (30분) ──────────────────────────────
def create_access_token(data: dict) -> str:
    """API 요청용 단기 신분증. 유효기간 30분."""
    return _create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


# ── Refresh Token 생성 (7일) ──────────────────────────────
def create_refresh_token(data: dict) -> str:
    """토큰 재발급용 장기 티켓. 유효기간 7일."""
    return _create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

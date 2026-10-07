# ───────────────────────────────────────────────────────────
# User 비즈니스 로직 (Service Layer)
# - create_user       : 이메일 중복 체크 + bcrypt 해시 + DB 저장
# - authenticate_user : 이메일/비밀번호 인증
# ───────────────────────────────────────────────────────────

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.core.security import hash_password, verify_password
from backend.domain.users.models.user import User
from backend.domain.users.schemas.user import UserCreate


# ── 회원가입 ─────────────────────────────────────────────
def create_user(db: Session, data: UserCreate) -> User:
    """
    1. 이메일 중복 체크 (중복 시 400 Bad Request)
    2. 비밀번호 bcrypt 해시화
    3. User ORM 객체 생성 후 DB 저장
    """
    # 이메일 중복 체크
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 이메일 주소입니다.",
        )

    # 비밀번호 해시화 (평문을 절대 DB에 저장하지 않음)
    hashed_pw = hash_password(data.password)

    # ORM 모델 생성 및 저장
    user = User(
        email=data.email,
        password=hashed_pw,
        terms_agreed=data.terms_agreed,
        privacy_agreed=data.privacy_agreed,
        marketing_agreed=data.marketing_agreed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── 로그인 인증 ───────────────────────────────────────────
def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    이메일 존재 여부 + 비밀번호 일치 여부 검증.
    보안을 위해 이메일/비밀번호 오류 모두 동일한 401 메시지 반환.
    """
    user = db.query(User).filter(User.email == email).first()

    # 이메일이 없거나 비밀번호 불일치 → 동일한 에러 메시지 (보안)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

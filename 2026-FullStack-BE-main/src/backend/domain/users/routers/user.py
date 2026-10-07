# ───────────────────────────────────────────────────────────
# Auth 라우터
# POST /auth/sign-up  → 회원가입 (201 Created)
# POST /auth/sign-in  → 로그인  (200 OK + JWT 토큰 쌍)
# ───────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import create_access_token, create_refresh_token
from backend.domain.users.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from backend.domain.users.services.user import authenticate_user, create_user

router = APIRouter(prefix="/auth", tags=["AUTH"])


# ── POST /auth/sign-up ────────────────────────────────────
@router.post(
    "/sign-up",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="이메일, 비밀번호, 약관 동의 정보를 받아 새로운 계정을 생성합니다.",
)
def sign_up(data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    - 이메일 중복 → 400 Bad Request
    - 필수 약관 미동의 → 422 Unprocessable Entity (Pydantic)
    - 성공 → 201 Created
    """
    user = create_user(db, data)
    return user


# ── POST /auth/sign-in ────────────────────────────────────
@router.post(
    "/sign-in",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="로그인",
    description="이메일과 비밀번호로 인증 후 Access/Refresh Token 쌍을 발급합니다.",
)
def sign_in(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    - 이메일 없음 / 비밀번호 불일치 → 401 Unauthorized (동일 메시지)
    - 성공 → access_token, refresh_token, token_type: bearer
    """
    user = authenticate_user(db, data.email, data.password)

    # JWT payload: sub에 이메일 저장 (표준 클레임)
    token_data = {"sub": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

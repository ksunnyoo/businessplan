# ───────────────────────────────────────────────────────────
# Pydantic 스키마 정의
# ───────────────────────────────────────────────────────────

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── 1. 회원가입 요청 스키마 ──────────────────────────────────
# 클라이언트가 POST /auth/sign-up 요청 시 보내는 데이터를 검증합니다.
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 주소", example="user@example.com")
    password: str = Field(..., min_length=8, description="사용자 비밀번호 (최소 8자)", example="securepass1")

    # 약관 동의 필드 (...  = 필수 입력)
    terms_agreed: bool = Field(..., description="서비스 이용약관 동의 (필수)", example=True)
    privacy_agreed: bool = Field(..., description="개인정보 처리방침 동의 (필수)", example=True)
    marketing_agreed: bool = Field(False, description="마케팅 정보 수신 동의 (선택)", example=False)

    # ── 필수 약관 유효성 검사 ────────────────────────────────
    # terms_agreed 또는 privacy_agreed 가 False 이면 422 Unprocessable Entity 반환
    @field_validator("terms_agreed")
    @classmethod
    def terms_must_be_agreed(cls, v: bool) -> bool:
        if not v:
            raise ValueError("서비스 이용약관에 동의해야 합니다.")
        return v

    @field_validator("privacy_agreed")
    @classmethod
    def privacy_must_be_agreed(cls, v: bool) -> bool:
        if not v:
            raise ValueError("개인정보 처리방침에 동의해야 합니다.")
        return v


# ── 2. 회원가입 성공 응답 스키마 ────────────────────────────
class UserResponse(BaseModel):
    id: int
    email: str
    terms_agreed: bool
    privacy_agreed: bool
    marketing_agreed: bool

    model_config = {"from_attributes": True}


# ── 3. 로그인 요청 스키마 ────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 주소", example="user@example.com")
    password: str = Field(..., description="사용자 비밀번호", example="securepass1")


# ── 4. 토큰 응답 스키마 ─────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

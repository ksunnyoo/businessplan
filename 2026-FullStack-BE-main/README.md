# 1인 예비창업자/초기창업자를 위한 AI 사업계획서 도출 플랫폼 — Backend

FastAPI + SQLAlchemy + Supabase(PostgreSQL) 기반의 인증 API 서버입니다.

---

## 🗂️ 프로젝트 구조

```
2026-FullStack-BE-main/
├── main.py                          # FastAPI 앱 진입점, CORS 설정
├── api.py                           # 중앙 라우터 (/api/v1)
├── .env.example                     # 환경변수 템플릿 (커밋용)
├── .env                             # 실제 환경변수 (절대 커밋 금지 ⚠️)
├── create_tables.py                 # DB 테이블 초기 생성 스크립트
└── src/backend/
    ├── core/
    │   ├── database.py              # DB 엔진, 세션, get_db() 의존성
    │   └── security.py             # bcrypt 해시, JWT 토큰 생성/검증
    └── domain/users/
        ├── models/user.py          # User ORM 모델
        ├── schemas/user.py         # Pydantic 스키마 (유효성 검증)
        ├── services/user.py        # 비즈니스 로직 (회원가입/인증)
        └── routers/user.py         # API 엔드포인트 라우터
```

---

## ⚙️ 환경 설정

### 1. `.env` 파일 생성

`.env.example`을 복사하여 실제 값을 채웁니다.

```bash
cp .env.example .env
```

`.env` 파일 내용:

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
SECRET_KEY=<openssl rand -hex 32 으로 생성>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> ⚠️ `.env` 파일은 절대 git에 커밋하지 마세요. `.gitignore`에 등록되어 있습니다.

### 2. 패키지 설치

```bash
# 가상환경 활성화 후
pip install bcrypt python-jose[cryptography] python-dotenv "psycopg[binary]"
```

### 3. DB 테이블 생성

```bash
PYTHONPATH=. python create_tables.py
```

---

## 🚀 서버 실행

```bash
PYTHONPATH=. uvicorn main:app --reload
```

서버 실행 후 접속:
- **Swagger UI**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api/v1

---

## 📡 API 엔드포인트

### `POST /api/v1/auth/sign-up` — 회원가입

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass1",
  "terms_agreed": true,
  "privacy_agreed": true,
  "marketing_agreed": false
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "terms_agreed": true,
  "privacy_agreed": true,
  "marketing_agreed": false
}
```

**에러 케이스:**
| 상태 코드 | 원인 |
|---|---|
| `400 Bad Request` | 이미 가입된 이메일 |
| `422 Unprocessable Entity` | 필수 약관 미동의 또는 입력값 형식 오류 |

---

### `POST /api/v1/auth/sign-in` — 로그인

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass1"
}
```

**Response `200 OK`:**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

**에러 케이스:**
| 상태 코드 | 원인 |
|---|---|
| `401 Unauthorized` | 이메일 없음 또는 비밀번호 불일치 (보안상 동일 메시지) |

---

## 🔐 보안 설계

| 항목 | 구현 방식 |
|---|---|
| 비밀번호 저장 | bcrypt 해시 (평문 절대 저장 안 함) |
| Access Token | JWT, 30분 만료 |
| Refresh Token | JWT, 7일 만료 |
| 로그인 실패 메시지 | 이메일/비밀번호 구분 없이 동일 메시지 (열거 공격 방지) |
| 환경변수 | `.env` 사용, git 제외 |

---

## 🛠️ 기술 스택

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **Database**: Supabase (PostgreSQL)
- **Auth**: JWT (python-jose) + bcrypt
- **Validation**: Pydantic v2

"""
DB 테이블 초기 생성 스크립트.
이 파일은 개발용이며, 실제 운영에서는 Alembic 마이그레이션을 사용하세요.
"""
from dotenv import load_dotenv
load_dotenv()

from src.backend.core.database import Base, engine
from src.backend.domain.users.models.user import User  # noqa: F401 (import for side-effect)

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! Tables created successfully.")

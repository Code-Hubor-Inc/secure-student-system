import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENCRYPTION_KEY", "test-encryption-key")
os.environ.setdefault("R2_ACCOUNT_ID", "test-account-id")
os.environ.setdefault("R2_ACCESS_KEY_ID", "test-access-key-id")
os.environ.setdefault("R2_SECRET_ACCESS_KEY", "test-secret-access-key")
os.environ.setdefault("R2_BUCKET_NAME", "test-bucket")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import app.models  # noqa: E402,F401
from app.db.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    fake_storage: dict[str, bytes] = {}

    def _upload_object(key: str, data: bytes) -> None:
        fake_storage[key] = data

    def _download_object(key: str) -> bytes:
        return fake_storage[key]

    def _delete_object(key: str) -> None:
        fake_storage.pop(key, None)

    monkeypatch.setattr("app.api.files.upload_object", _upload_object)
    monkeypatch.setattr("app.api.files.download_object", _download_object)
    monkeypatch.setattr("app.api.files.delete_object", _delete_object)
    return fake_storage

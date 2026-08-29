import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.core.config import settings
from app.db.database import Base, get_db
from app.main import app as fastapi_app


@pytest.fixture()
def db_session(tmp_path):
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    settings.UPLOAD_DIR = str(tmp_path)

    yield TestingSessionLocal()

    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def client(db_session):
    return TestClient(fastapi_app)

@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    fake_storage = {}

    def fake_upload(key, data):
        fake_storage[key] = data

    def fake_download(key):
        return fake_storage[key]

    def fake_delete(key):
        fake_storage.pop(key, None)

    monkeypatch.setattr("app.api.files.upload_object", fake_upload)
    monkeypatch.setattr("app.api.files.download_object", fake_download)
    monkeypatch.setattr("app.api.files.delete_object", fake_delete)
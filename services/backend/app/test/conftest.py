from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..db.session import AsyncSession
from ...main import app


@pytest.fixture(scope="session")
def db() -> AsyncGenerator:
    yield AsyncSession()


@pytest.fixture(scope="module")
def client() -> AsyncGenerator:
    with TestClient(app) as c:
        yield c


import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from httpx import AsyncClient
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT
from src.main import app
from src.models.models import Base

@pytest.fixture(scope="module")
async def temp_db():
    test_db_name = "your_test_db_name"
    test_db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{test_db_name}"

    if not database_exists(test_db_url):
        create_database(test_db_url)

    test_engine = create_async_engine(test_db_url)
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_session  # Возвращаем сессию для использования в тестах

    # Удаляем базу данных после тестов
    drop_database(test_db_url)

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client  # Передаем экземпляр AsyncClient

@pytest.mark.asyncio
async def test_generate(client, temp_db):
    request_data = {
        "secret": "my_secret",
        "code_phrase": "my_code_phrase",
        "TTL": 10
    }

    response = await client.post("/generate", json=request_data)

    assert response.status_code == 200
    # Дополнительные проверки можно добавить здесь
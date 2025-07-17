import pytest
import asyncio
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests at the session level."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def async_client() -> AsyncClient:
    """Create an asynchronous HTTP client to send requests to the application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

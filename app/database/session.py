from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

# --- Synchronous part (Sync) for LangChain tools ---
# This engine is used for tools that require synchronous query execution.
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    pool_pre_ping=True,  # Check connection before each query
)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# --- Asynchronous part (Async) for FastAPI ---
# This engine is used for asynchronous operations in FastAPI endpoints.
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,  # Disable query logging
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent objects from expiring after commit
    autocommit=False,
    autoflush=False,
)

# Dependency to inject into FastAPI endpoints
async def get_db() -> AsyncSession:
    """
    A FastAPI dependency that provides an asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session

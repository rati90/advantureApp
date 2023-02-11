from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:22585@localhost:5432/postgres"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,future=True) # echo=True,

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
)


mapper_registry = registry()
Base = mapper_registry.generate_base()


async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()

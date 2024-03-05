import asyncio
from contextlib import asynccontextmanager

import asyncpg
from redis import asyncio as aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from deps import DatabaseConnectionMarker, SettingsMarker
from routers import products

import dotenv
import os

from settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = app.dependency_overrides[SettingsMarker]()

    connection = await asyncpg.connect(
        f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
    )

    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    app.dependency_overrides.update(
        {
            DatabaseConnectionMarker: lambda: connection
        }
    )

    yield

    await connection.close()


def register_app(settings: Settings) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings
        }
    )

    app.include_router(products.router, prefix="/products")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=settings.cors_allowed_methods,
        allow_headers=settings.cors_allowed_headers
    )

    return app


def main():
    dotenv.load_dotenv()

    settings = Settings(
        db_name=os.getenv(key="DB_NAME"),
        db_host=os.getenv(key="DB_HOST"),
        db_user=os.getenv(key="DB_USER"),
        db_password=os.getenv(key="DB_PASSWORD"),
        cors_allowed_origins=os.getenv("ALLOWED_ORIGINS").split(","),
        cors_allowed_methods=os.getenv("ALLOWED_METHODS").split(","),
        cors_allowed_headers=os.getenv("ALLOWED_HEADERS").split(","),
        redis_host=os.getenv("REDIS_HOST"),
        redis_port=int(os.getenv("REDIS_PORT")),
    )

    app = register_app(settings=settings)

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    main()

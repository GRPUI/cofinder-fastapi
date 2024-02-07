import asyncio
from contextlib import asynccontextmanager

import asyncpg
import uvicorn
from fastapi import FastAPI
from deps import DatabaseConnectionMarker
from routers import products

import dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    dotenv.load_dotenv()
    database = os.getenv(key="DB_NAME")
    user = os.getenv(key="DB_USER")
    password = os.getenv(key="DB_PASSWORD")
    host = os.getenv(key="DB_HOST")

    connection = await asyncpg.connect(
        f"postgresql://{user}:{password}@{host}/{database}"
    )

    app.dependency_overrides.update(
        {
            DatabaseConnectionMarker: lambda: connection
        }
    )

    yield

    await connection.close()


def register_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(products.router, prefix="/products")

    return app


def main():
    app = register_app()

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    main()

import asyncio
from contextlib import asynccontextmanager

import asyncpg
import uvicorn
from fastapi import FastAPI
from deps import DatabaseConnectionMarker
from routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):

    connection = await asyncpg.connect(
        "postgresql://cofinder:j8FAC2DBYWZpvGNknPKR4uTwybtfxUcemqsMad73X6L5Q9gzHS@localhost/postgres"
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
        host="localhost",
        port=8000
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    main()

from asyncpg import Connection
from fastapi import APIRouter, Depends

from deps import DatabaseConnectionMarker
from services import products

router = APIRouter()


@router.get("/")
async def root(
    connection: Connection = Depends(DatabaseConnectionMarker)
):
    return await products.get_main_page(connection)


@router.get("/category/{category_id}")
async def get_products_by_category(category_id: int, connection: Connection = Depends(DatabaseConnectionMarker)):
    return await products.get_products_by_category(category_id, connection)


@router.get("/{product_id}")
async def get_product(product_id: int, connection: Connection = Depends(DatabaseConnectionMarker)):
    return await products.get_product(product_id, connection)

from asyncpg import Connection
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from deps import DatabaseConnectionMarker
from models.product import AddProductModel
from services import products

router = APIRouter()


@router.get("/")
async def root(
    connection: Connection = Depends(DatabaseConnectionMarker)
):
    return await products.get_main_page(connection)


@router.get("/category/{category_id}")
@cache(expire=600)
async def get_products_by_category(category_id: int, connection: Connection = Depends(DatabaseConnectionMarker)):
    return await products.get_products_by_category(category_id, connection)


@router.get("/categories")
@cache(expire=3600)
async def get_categories(connection: Connection = Depends(DatabaseConnectionMarker)):
    return await products.get_categories(connection)


@router.get("/{product_id}")
@cache(600)
async def get_product(product_id: int, connection: Connection = Depends(DatabaseConnectionMarker)):
    return await products.get_product(product_id, connection)


@router.get("/search/{query}")
@cache(600)
async def get_search_results(
    query: str,
    connection: Connection = Depends(DatabaseConnectionMarker)
):
    if not query:
        return []
    return await products.get_search_results(query, connection)


@router.post("/add/")
async def add_product(
    product: AddProductModel,
    connection: Connection = Depends(DatabaseConnectionMarker)
):
    return await products.add_product(connection, product)

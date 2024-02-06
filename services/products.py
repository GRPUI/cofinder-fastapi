from typing import List, Dict, Any

from asyncpg import Connection


async def get_lowest_price_source(
        connection: Connection,
        product_id: int) -> str:
    source = await connection.fetchval("""SELECT source FROM prices
            WHERE product = $1
            GROUP BY source 
            ORDER BY MIN(price) DESC, MAX(date) 
            LIMIT 1;""", product_id)
    return source


async def get_all_sources(
        connection: Connection,
        product_id: int) -> List[str]:
    sources = await connection.fetch("""SELECT source FROM prices
            WHERE product = $1
            GROUP BY source 
            ORDER BY MAX(date) DESC;""", product_id)
    return list(map(lambda x: x[0], sources))


async def get_newest_price_by_source(
        connection: Connection,
        product_id: int,
        source: str) -> int:
    price = await connection.fetchval(f"""SELECT price, source, link FROM prices
        WHERE product = $1 and source = $2
        ORDER BY date DESC 
        LIMIT 1;""", product_id, source)

    return price


async def get_mini_card_info(
        connection: Connection,
        product_id: int,
        source: str) -> Dict[str, Any]:
    product_props = await connection.fetchrow("""SELECT product, name, price, products.image FROM prices
    INNER JOIN products ON products.id = prices.product
    WHERE product = $1 AND source = $2
    ORDER BY date DESC
    LIMIT 1;""", product_id, source)
    print(product_props)
    if product_props is None:
        return {}
    product_props = zip(("id", "name", "price", "link"), product_props)
    return dict(product_props)


async def get_main_page(
    connection: Connection
) -> List[Dict[str, Any]]:
    product_ids = await connection.fetch("""SELECT id FROM products
                ORDER BY RANDOM()
                LIMIT 10;""")

    products_ids = list(map(lambda x: x[0], product_ids))
    products = []
    for product_id in products_ids:
        source = await get_lowest_price_source(connection, product_id)
        product_props = await get_mini_card_info(connection, product_id, source)
        products.append(product_props)

    return products


async def get_products_by_category(
    category_id: int,
    connection: Connection
) -> List[Dict[str, Any]]:
    product_ids = await connection.fetch("""SELECT products.id FROM products
    INNER JOIN categories ON categories.id = products.category
    WHERE categories.id = $1;""", category_id)

    products_ids = list(map(lambda x: x[0], product_ids))
    products = []
    for product_id in products_ids:
        source = await get_lowest_price_source(connection, product_id)
        product_props = await get_mini_card_info(connection, product_id, source)
        products.append(product_props)

    return products


async def get_product(
    product_id: int,
    connection: Connection
) -> Dict[str, Any]:
    sources = await get_all_sources(connection, product_id)
    full_price_info = await connection.fetchrow("""SELECT products.id, products.name, categories.name, 
    products.description, products.image FROM products
    INNER JOIN categories ON products.category = categories.id
    WHERE products.id = $1;""", product_id)

    prices = []

    for source in sources:
        price = await get_newest_price_by_source(connection, product_id, source)
        prices.append({source: price})

    product_props = dict(zip(("id", "name", "category", "description", "image"), tuple(full_price_info)))
    product_props["prices"] = prices
    return product_props

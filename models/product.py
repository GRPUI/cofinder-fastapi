from pydantic import BaseModel


class AddProductModel(BaseModel):
    name: str
    category: int
    description: str = None
    image: str = None

    price: float
    source: str
    link: str

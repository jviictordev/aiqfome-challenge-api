from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, EmailStr, RootModel


class ProductsSchema(BaseModel):
    id: int
    title: str
    image: str
    price: float
    review: str

class AllProductsSchema(RootModel[List[ProductsSchema]]):
    pass
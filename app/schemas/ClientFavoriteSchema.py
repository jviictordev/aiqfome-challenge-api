from uuid import UUID
from typing import List
from pydantic import BaseModel, RootModel


class CreateClientFavoriteSchema(BaseModel):
    client_id: UUID
    product_id: int

class DeleteClientFavoriteSchema(BaseModel):
    message: str

class ClientFavoriteResponseSchema(BaseModel):
    id: int
    title: str
    image: str
    price: float
    review: str

class AllClientsResponseSchema(RootModel[List[ClientFavoriteResponseSchema]]):
    pass
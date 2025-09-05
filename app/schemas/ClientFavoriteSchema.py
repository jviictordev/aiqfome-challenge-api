from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateClientFavoriteSchema(BaseModel):
    client_id: UUID
    product_id: int

class ListClientFavoriteSchema(BaseModel):
    client_id: UUID

class DeleteClientFavoriteSchema(BaseModel):
    client_id: UUID
    product_id: int

class UpdateClientSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientFavoriteResponseSchema(BaseModel):
    id: int
    title: str
    image: str
    price: float
    review: str

class AllClientsResponseSchema(BaseModel):
    client_favorites: List[ClientFavoriteResponseSchema]
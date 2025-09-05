from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClientSchema(BaseModel):
    name: str
    email: EmailStr

class DeleteClientSchema(BaseModel):
    id: UUID

class UpdateClientSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientResponseSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr

class AllClientsResponseSchema(BaseModel):
    clients: List[ClientSchema]
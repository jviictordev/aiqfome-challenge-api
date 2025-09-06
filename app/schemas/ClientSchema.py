from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, EmailStr, RootModel


class ClientSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: int

class ClientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: int

class DeleteClientSchema(BaseModel):
    message: str

class UpdateClientSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class AllClientsResponseSchema(RootModel[List[ClientSchema]]):
    pass
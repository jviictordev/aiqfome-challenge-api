from enum import IntEnum
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, EmailStr, RootModel, validator


class ClientRoles(IntEnum):
    ADMIN = 1
    USER = 2

class ClientSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: ClientRoles

class ClientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: ClientRoles

class DeleteClientSchema(BaseModel):
    message: str

class UpdateClientSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class AllClientsResponseSchema(RootModel[List[ClientSchema]]):
    pass
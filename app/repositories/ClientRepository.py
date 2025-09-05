from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from uuid import UUID
from app.schemas.ClientFavoriteSchema import UpdateClientSchema
from app.config.Database import get_session
from app.models.Models import ClientModel

class ClientRepository:
    def __init__(self, session):
        self.session = session

    def add(self, client: ClientModel) -> ClientModel:
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client
    
    def update_client(self, client: ClientModel, new_client: UpdateClientSchema) -> ClientModel:
        client.name = new_client.name if new_client.name else client.name
        client.email = new_client.email if new_client.email else client.email
        self.session.commit()
        self.session.refresh(client)
        return client

    # Buscar um cliente pelo id
    def get_by_client_id(self, client_id: UUID) -> ClientModel:
        return self.session.scalar(
            select(ClientModel).where(ClientModel.id == client_id)
        )
    
    # Buscar um cliente pelo email
    def get_by_client_email(self, client_email: str) -> ClientModel:
        return self.session.scalar(
            select(ClientModel).where(ClientModel.email == client_email)
        )
    
    # Buscar todos os clientes
    def get_all_clients(self) -> List[ClientModel]:
        return self.session.scalars(
            select(ClientModel)
        ).all()

    # Remover um cliente
    def remove(self, client_id: UUID) -> bool:
        result = self.session.execute(
            delete(ClientModel).where(
                (ClientModel.id == client_id)
            )
        )
        self.session.commit()
        return result.rowcount > 0
    
def get_client_repository(session: Session = Depends(get_session)) -> ClientRepository:
    return ClientRepository(session)

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from uuid import UUID
from app.config.Database import get_session
from app.models.Models import ClientFavoriteModel

class ClientFavoriteRepository:
    def __init__(self, session):
        self.session = session

    def add(self, favorite: ClientFavoriteModel) -> ClientFavoriteModel:
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)
        return favorite

    # Buscar todos os favoritos de um cliente
    def get_by_client(self, client_id: UUID) -> List[ClientFavoriteModel]:
        return self.session.scalars(
            select(ClientFavoriteModel).where(ClientFavoriteModel.client_id == client_id)
        ).all()

    # Buscar um favorito específico (client + product)
    def get_by_client_and_product(self, client_id: UUID, product_id: int) -> Optional[ClientFavoriteModel]:
        return self.session.scalar(
            select(ClientFavoriteModel).where(
                (ClientFavoriteModel.client_id == client_id) &
                (ClientFavoriteModel.product_id == product_id)
            )
        )

    # Remover um favorito
    def remove(self, client_id: UUID, product_id: int) -> bool:
        result = self.session.execute(
            delete(ClientFavoriteModel).where(
                (ClientFavoriteModel.client_id == client_id) &
                (ClientFavoriteModel.product_id == product_id)
            )
        )
        self.session.commit()
        return result.rowcount > 0
    
def get_client_favorite_repository(session: Session = Depends(get_session)) -> ClientFavoriteRepository:
    return ClientFavoriteRepository(session)

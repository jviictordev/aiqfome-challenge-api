from uuid import UUID
from fastapi import Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.config.Database import get_session
from app.models.Models import ClientFavoriteModel


class ClientFavoriteRepository:
    def __init__(self, session):
        self.session = session

    def add_client_favorite(self, favorite: ClientFavoriteModel) -> ClientFavoriteModel:
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)
        return favorite

    def get_by_client_id(self, client_id: UUID) -> List[ClientFavoriteModel]:
        return self.session.scalars(
            select(ClientFavoriteModel).where(ClientFavoriteModel.client_id == client_id)
        ).all()

    def get_by_client_id_and_product_id(self, client_id: UUID, product_id: int) -> Optional[ClientFavoriteModel]:
        return self.session.scalar(
            select(ClientFavoriteModel).where(
                (ClientFavoriteModel.client_id == client_id) &
                (ClientFavoriteModel.product_id == product_id)
            )
        )

    def remove_client_favorite(self, client_id: UUID, product_id: int) -> bool:
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

from http import HTTPStatus
import json
from uuid import UUID
from fastapi import Depends, HTTPException
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from repositories.ClientRepository import ClientRepository, get_client_repository
from schemas.ClientFavoriteSchema import ClientFavoriteResponseSchema, UpdateClientSchema
from config.Database import get_session
from models.Models import ClientFavoriteModel, ClientModel
from repositories.ClientFavoriteRepository import ClientFavoriteRepository, get_client_favorite_repository


class ClientService:
    def __init__(self, client_favorite_repository: ClientFavoriteRepository, client_repository: ClientRepository):
        self.client_repository = client_repository
        self.client_favorite_repository = client_favorite_repository

    def add_client(self, client_name: str, client_email: str):
        """
        Adiciona um item aos favoritos do cliente.
        """
        client_exist = self.client_repository.get_by_client_email(client_email)

        if client_exist:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já existe um cliente com esse email.',
            )
        client_model = ClientModel(
            name=client_name,
            email=client_email
        )
        return self.client_repository.add(client_model)

    def remove_client(self, client_id: UUID) -> str:
        """
        Remove um cliente.
        """
        removed_message = 'Cliente excluído com sucesso.'
        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )
        removed_client = self.client_repository.remove(client_id)
        removed_message = removed_message if removed_client else 'Falha ao excluir o cliente.'
        return removed_message

    def list_clients(self):
        clients = self.client_repository.get_all_clients()
        return clients
    
    def update_client(self, client_id:UUID, new_client: UpdateClientSchema):
        client_to_update = self.client_repository.get_by_client_id(client_id)
        if not client_to_update:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='Usuário não encontrado para atualizar.',
                )
        return self.client_repository.update_client(client_to_update, new_client)
    
def get_client_service(
    client_favorite_repository: ClientFavoriteRepository = Depends(get_client_favorite_repository),
    client_repository: ClientRepository = Depends(get_client_repository)
) -> ClientService:
    return ClientService(client_favorite_repository, client_repository)
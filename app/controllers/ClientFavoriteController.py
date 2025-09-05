import json
import requests

from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.ClientFavoriteSchema import AllClientsResponseSchema, ClientFavoriteResponseSchema, CreateClientFavoriteSchema, ListClientFavoriteSchema
from app.config.Database import get_session
from app.models.Models import ClientFavoriteModel, ClientModel
from app.services.ClientFavoriteService import ClientFavoriteService, get_client_favorite_service

client_favorite_router = APIRouter()



@client_favorite_router.post(
    '/client_favorite/create',
    status_code=HTTPStatus.CREATED,
    response_model=CreateClientFavoriteSchema
)
def create_client_favorite(
    client_id: UUID,
    product_id: int,
    client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service)
):
    return client_favorite_service.add_favorite(client_id, product_id)

@client_favorite_router.get(
    '/client_favorite/list',
    status_code=HTTPStatus.OK,
    response_model=AllClientsResponseSchema
)
def list_client_favorite(
    client_id: UUID,
    client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service)
):
    favorites_list = client_favorite_service.list_favorites(client_id)
    return {'client_favorites': favorites_list}

@client_favorite_router.delete(
    '/client_favorite/delete',
    status_code=HTTPStatus.OK
)
def delete_client_favorite(
    client_id: UUID,
    product_id: int,
    client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service)
):
    client_favorite_service.remove_favorite(client_id, product_id)
    return{'message': 'Produto favorito excluído com sucesso.'}
from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.models.Models import ClientModel
from app.services.ClientService import get_current_client
from app.services.ClientFavoriteService import ClientFavoriteService, get_client_favorite_service
from app.schemas.ClientFavoriteSchema import AllClientsResponseSchema, CreateClientFavoriteSchema, DeleteClientFavoriteSchema

client_favorite_router = APIRouter(tags=["ClientFavorite"])


@client_favorite_router.post('/client_favorite/create', status_code=HTTPStatus.CREATED, response_model=CreateClientFavoriteSchema)
def create_client_favorite(client_id: UUID, product_id: int, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service), logged_client: ClientModel = Depends(get_current_client)):
    client_favorite = client_favorite_service.add_client_favorite(client_id, product_id, logged_client.id)
    return CreateClientFavoriteSchema(
        client_id=client_favorite.client_id,
        product_id=client_favorite.product_id
    )

@client_favorite_router.get('/client_favorite/list', status_code=HTTPStatus.OK, response_model=AllClientsResponseSchema)
def list_client_favorite(client_id: UUID, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service)):
    return client_favorite_service.list_client_favorites(client_id)

@client_favorite_router.delete('/client_favorite/delete', status_code=HTTPStatus.OK, response_model=DeleteClientFavoriteSchema)
def delete_client_favorite(client_id: UUID, product_id: int, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service), logged_client: ClientModel = Depends(get_current_client)):
    removed_message = client_favorite_service.remove_client_favorite(client_id, product_id, logged_client.id)
    return DeleteClientFavoriteSchema(
        message=removed_message
    )
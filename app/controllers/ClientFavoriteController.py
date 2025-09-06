from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.models.Models import ClientModel
from app.services.ClientService import get_current_client
from app.services.ClientFavoriteService import ClientFavoriteService, get_client_favorite_service
from app.schemas.ClientFavoriteSchema import AllClientsResponseSchema, CreateClientFavoriteSchema, DeleteClientFavoriteSchema

client_favorite_router = APIRouter(tags=["ClientFavorite"], prefix='/client_favorite')


@client_favorite_router.post(
    path='/create',
    status_code=HTTPStatus.CREATED,
    response_model=CreateClientFavoriteSchema,
    summary="Rota para criar um produto favorito de um cliente",
    description="O cliente logado pode criar produtos favoritos, apenas para si mesmo."
)
def create_client_favorite(client_id: UUID, product_id: int, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service), logged_client: ClientModel = Depends(get_current_client)):
    client_favorite = client_favorite_service.add_client_favorite(client_id, product_id, logged_client.id)
    return CreateClientFavoriteSchema(
        client_id=client_favorite.client_id,
        product_id=client_favorite.product_id
    )

@client_favorite_router.get(
    path='/list',
    status_code=HTTPStatus.OK,
    response_model=AllClientsResponseSchema,
    summary="Rota para listar os produtos favoritos",
    description="A listagem apresentará apenas os produtos favoritados pelo cliente logado."
)
def list_client_favorite(client_id: UUID, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service)):
    return client_favorite_service.list_client_favorites(client_id)

@client_favorite_router.delete(
    path='/delete',
    status_code=HTTPStatus.OK,
    response_model=DeleteClientFavoriteSchema,
    summary="Rota para deletar um produto favorito",
    description="O cliente logado, só pode remover um produto da sua própria lista de favoritos."
)
def delete_client_favorite(client_id: UUID, product_id: int, client_favorite_service: ClientFavoriteService = Depends(get_client_favorite_service), logged_client: ClientModel = Depends(get_current_client)):
    removed_message = client_favorite_service.remove_client_favorite(client_id, product_id, logged_client.id)
    return DeleteClientFavoriteSchema(
        message=removed_message
    )
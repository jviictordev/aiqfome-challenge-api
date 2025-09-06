from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.ClientService import ClientService, get_client_service, get_current_client, require_admin
from app.config.Database import get_session
from app.config.Auth import create_access_token, verify_password, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.Models import ClientModel
from app.schemas.ClientSchema import AllClientsResponseSchema, ClientResponseSchema, CreateClientSchema, DeleteClientSchema, UpdateClientSchema

client_router = APIRouter(tags=["Client"])


@client_router.post(
    '/client/create',
    status_code=HTTPStatus.CREATED,
    response_model=ClientResponseSchema
)
def create_client(
    client: CreateClientSchema,
    client_service: ClientService = Depends(get_client_service),
    admin_client: ClientModel = Depends(require_admin)
):
    return client_service.add_client(client.name, client.email, hash_password(client.password), client.role)

@client_router.get(
    '/client/list_all',
    status_code=HTTPStatus.OK,
    response_model=AllClientsResponseSchema
)
def get_clients(
    client_service: ClientService = Depends(get_client_service)
):  
    clients = client_service.list_clients()
    return {'clients': clients}

@client_router.get(
    '/client/list',
    status_code=HTTPStatus.OK,
    response_model=ClientResponseSchema
)
def get_client(
    client_id: UUID,
    client_service: ClientService = Depends(get_client_service)
):  
    return client_service.list_client(client_id)

@client_router.delete(
    '/client/delete',
    status_code=HTTPStatus.OK
)
def delete_client(
    client_id: UUID,
    client_service: ClientService = Depends(get_client_service),
    admin_client: ClientModel = Depends(require_admin)
):
    removed_message = client_service.remove_client(client_id)
    return {'message': removed_message}

@client_router.patch(
    '/client/update',
    status_code=HTTPStatus.OK,
    response_model=ClientResponseSchema
)
def update_client(
    client: UpdateClientSchema,
    client_id: UUID,
    client_service: ClientService = Depends(get_client_service),
    logged_client: ClientModel = Depends(get_current_client)
):
    return client_service.update_client(client_id, client, logged_client.id)
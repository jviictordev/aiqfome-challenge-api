from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.ClientService import ClientService, get_client_service
from app.config.Database import get_session
from app.models.Models import ClientModel
from app.schemas.ClientSchema import AllClientsResponseSchema, ClientResponseSchema, ClientSchema, DeleteClientSchema, UpdateClientSchema

client_router = APIRouter()


@client_router.post(
    '/client/create',
    status_code=HTTPStatus.CREATED,
    response_model=ClientResponseSchema
)
def create_client(
    client: ClientSchema,
    client_service: ClientService = Depends(get_client_service)
):
    return client_service.add_client(client.name, client.email)

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
    client_service: ClientService = Depends(get_client_service)
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
    client_service: ClientService = Depends(get_client_service)
):
    return client_service.update_client(client_id, client)
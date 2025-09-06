from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.config.Auth import hash_password
from app.models.Models import ClientModel
from app.services.ClientService import ClientService, get_client_service, get_current_client, require_admin
from app.schemas.ClientSchema import AllClientsResponseSchema, ClientCreateSchema, ClientSchema, DeleteClientSchema, UpdateClientSchema

client_router = APIRouter(tags=["Client"])


@client_router.post('/client/create', status_code=HTTPStatus.CREATED, response_model=ClientSchema)
def create_client(client: ClientCreateSchema, client_service: ClientService = Depends(get_client_service), admin_client: ClientModel = Depends(require_admin)):
    created_client = client_service.add_client(client.name, client.email, hash_password(client.password), client.role)
    return ClientSchema(
        id=created_client.id,
        name=created_client.name,
        email=created_client.email,
        role=created_client.role
    )

@client_router.get('/client/list_all', status_code=HTTPStatus.OK, response_model=AllClientsResponseSchema)
def get_clients(client_service: ClientService = Depends(get_client_service)):  
    return client_service.list_clients()

@client_router.get('/client/list', status_code=HTTPStatus.OK, response_model=ClientSchema)
def get_client(client_id: UUID, client_service: ClientService = Depends(get_client_service)):  
    client = client_service.list_client(client_id)
    return ClientSchema(
        id=client.id,
        name=client.name,
        email=client.email,
        role=client.role
    )

@client_router.delete('/client/delete', status_code=HTTPStatus.OK, response_model=DeleteClientSchema)
def delete_client(client_id: UUID, client_service: ClientService = Depends(get_client_service), admin_client: ClientModel = Depends(require_admin)):
    removed_message = client_service.remove_client(client_id)
    return DeleteClientSchema(message=removed_message)

@client_router.patch('/client/update', status_code=HTTPStatus.OK, response_model=ClientSchema)
def update_client(client: UpdateClientSchema, client_id: UUID, client_service: ClientService = Depends(get_client_service), logged_client: ClientModel = Depends(get_current_client)):
    client = client_service.update_client(client_id, client, logged_client.id)
    return ClientSchema(
        id=client.id,
        name=client.name,
        email=client.email,
        role=client.role
    )
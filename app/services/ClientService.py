import uuid
from uuid import UUID
from http import HTTPStatus
from app.models.Models import ClientModel
from fastapi import Depends, HTTPException
from app.schemas.ClientSchema import UpdateClientSchema
from app.config.Auth import decode_access_token, hash_password
from app.repositories.ClientRepository import ClientRepository, get_client_repository
from app.repositories.ClientFavoriteRepository import ClientFavoriteRepository, get_client_favorite_repository


class ClientService:
    def __init__(self, client_favorite_repository: ClientFavoriteRepository, client_repository: ClientRepository):
        self.client_repository = client_repository
        self.client_favorite_repository = client_favorite_repository

    def add_client(self, client_name: str, client_email: str, client_password: str, client_role: int):
        client_exist = self.client_repository.get_by_client_email(client_email)

        if client_exist:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já existe um cliente com esse email.',
            )
        
        if not client_password or not client_email or not client_role or not client_name:
             raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Algumas informações do usuário estão vazias.',
            )

        client_model = ClientModel(
            id=uuid.uuid4(),
            name=client_name,
            email=client_email,
            password=hash_password(client_password),
            role=client_role
        )
        return self.client_repository.add_client(client_model)

    def remove_client(self, client_id: UUID) -> str:
        removed_message = 'Cliente excluído com sucesso.'
        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )
        removed_client = self.client_repository.remove_client(client_id)
        removed_message = removed_message if removed_client else 'Falha ao excluir o cliente.'
        return removed_message

    def list_clients(self):
        clients = self.client_repository.get_all_clients()
        return clients
    
    def list_client(self, client_id):
        client = self.client_repository.get_by_client_id(client_id)
        if not client:
            raise HTTPException(
                    status_code=HTTPStatus.NO_CONTENT,
                    detail='Usuário não encontrado.',
                )
        return client
    
    def update_client(self, client_id:UUID, new_client: UpdateClientSchema, logged_client_id: UUID):
        if not client_id == logged_client_id:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='Usuário não tem permissão para efetuar atualização de outro usuário.',
                )
        client_to_update = self.client_repository.get_by_client_id(client_id)
        if not client_to_update:
                raise HTTPException(
                    status_code=HTTPStatus.NO_CONTENT,
                    detail='Usuário não encontrado para atualizar.',
                )
        
        check_email = self.client_repository.get_by_client_email(new_client.email)
        if check_email:
             raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já existe um usuário com esse email.',
            )

        return self.client_repository.update_client(client_to_update, new_client)
    
def get_client_service(
    client_favorite_repository: ClientFavoriteRepository = Depends(get_client_favorite_repository),
    client_repository: ClientRepository = Depends(get_client_repository)
) -> ClientService:
    return ClientService(client_favorite_repository, client_repository)

def get_current_client(client_service: ClientService = Depends(get_client_service), payload: dict = Depends(decode_access_token)):
    client = client_service.list_client(payload.get('sub'))
    return client

def require_admin(client: dict = Depends(get_current_client)):
    if client.role != 1:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Cliente sem permissão para executar essa ação."
        )
    return client
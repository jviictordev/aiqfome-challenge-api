import json
from uuid import UUID
from http import HTTPStatus
from fastapi import Depends, HTTPException
from app.models.Models import ClientFavoriteModel
from app.schemas.ClientFavoriteSchema import ClientFavoriteResponseSchema
from app.repositories.ClientRepository import ClientRepository, get_client_repository
from app.repositories.FakeStoreRepository import FakeStoreRepository, get_fake_store_repository
from app.repositories.ClientFavoriteRepository import ClientFavoriteRepository, get_client_favorite_repository


class ClientFavoriteService:
    def __init__(self, client_favorite_repository: ClientFavoriteRepository, client_repository: ClientRepository, fake_store_repository: FakeStoreRepository):
        self.client_repository = client_repository
        self.fake_store_repository = fake_store_repository
        self.client_favorite_repository = client_favorite_repository

    def add_client_favorite(self, client_id: UUID, product_id: int, logged_client_id: UUID):
        if not client_id == logged_client_id:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='Usuário não tem permissão para favoritar produtos para outro usuário.',
                )

        product_exist = self.client_favorite_repository.get_by_client_id_and_product_id(client_id, product_id)

        if product_exist:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Esse produto ja está vinculado à esse cliente.',
            )

        product_is_valid = self.fake_store_repository.get_by_product_id(product_id)

        if product_is_valid.status_code != HTTPStatus.OK or not product_is_valid.text:
            raise HTTPException(
                status_code= HTTPStatus.BAD_REQUEST,
                detail='O produto não pode ser validado.'
            )
        
        product_favorite = ClientFavoriteModel(
            client_id=client_id, product_id=product_id
        )
        return self.client_favorite_repository.add_client_favorite(product_favorite)

    def remove_client_favorite(self, client_id, product_id, logged_client_id: UUID):
        """
        Remove um item dos favoritos do cliente.
        """
        removed_message = 'Produto favorito excluído com sucesso.'
        if not client_id == logged_client_id:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='Usuário não tem permissão para deletar produtos de outro usuário.',
                )

        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )

        product_exist = self.client_favorite_repository.get_by_client_id_and_product_id(client_id, product_id)
        
        if not product_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Produto não encontrado na lista de favoritos do cliente.',
            )
        removed_client_favorite = self.client_favorite_repository.remove_client_favorite(client_id, product_id)
        removed_message = removed_message if removed_client_favorite else 'Falha ao excluir o produto favorito.'
        return removed_message

    def list_client_favorites(self, client_id):
        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )

        favorites_list = self.client_favorite_repository.get_by_client_id(client_id)
        if not favorites_list:
            raise HTTPException(
                status_code=HTTPStatus.NO_CONTENT,
                detail='Não existe nenhum produto favorito vinculado à este cliente.',
            )
        
        favorites_list_formated = []
        for fav in favorites_list:
            product_data = self.fake_store_repository.get_by_product_id(fav.product_id)
            if product_data.status_code != HTTPStatus.OK or not product_data.text:
                raise HTTPException(
                    status_code= HTTPStatus.BAD_REQUEST,
                    detail=f'O produto {fav.product_id} não pode ser validado.'
                )
            product_data = json.loads(product_data.text)
            favorites_list_formated.append(
                ClientFavoriteResponseSchema(
                    id=product_data.get('id'),
                    title=product_data.get('title'),
                    price=product_data.get('price'),
                    image=product_data.get('image'),
                    review=product_data.get('review', '')
                )
            )

        return favorites_list_formated
    
def get_client_favorite_service(
    client_favorite_repository: ClientFavoriteRepository = Depends(get_client_favorite_repository),
    client_repository: ClientRepository = Depends(get_client_repository),
    fake_store_repository: FakeStoreRepository = Depends(get_fake_store_repository)
) -> ClientFavoriteService:
    return ClientFavoriteService(client_favorite_repository, client_repository, fake_store_repository)
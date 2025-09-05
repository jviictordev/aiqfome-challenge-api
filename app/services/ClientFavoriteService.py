from http import HTTPStatus
import json
from uuid import UUID
from fastapi import Depends, HTTPException
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from repositories.ClientRepository import ClientRepository, get_client_repository
from schemas.ClientFavoriteSchema import ClientFavoriteResponseSchema
from config.Database import get_session
from models.Models import ClientFavoriteModel
from repositories.ClientFavoriteRepository import ClientFavoriteRepository, get_client_favorite_repository


class ClientFavoriteService:
    def __init__(self, client_favorite_repository: ClientFavoriteRepository, client_repository: ClientRepository):
        self.client_repository = client_repository
        self.client_favorite_repository = client_favorite_repository

    def add_favorite(self, client_id: UUID, product_id: int):
        """
        Adiciona um item aos favoritos do cliente.
        """
        product_exist = self.client_favorite_repository.get_by_client_and_product(client_id, product_id)

        if product_exist:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Esse produto ja está vinculado à esse cliente.',
            )

        product_is_valid = requests.get(f'https://fakestoreapi.com/products/{product_id}')

        if product_is_valid.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code= product_is_valid.status_code,
                detail='O produto não pode ser validado.'
            )
        
        product_favorite = ClientFavoriteModel(
            client_id=client_id, product_id=product_id
        )
        return self.client_favorite_repository.add(product_favorite)

    def remove_favorite(self, client_id, product_id):
        """
        Remove um item dos favoritos do cliente.
        """
        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )

        product_exist = self.client_favorite_repository.get_by_client_and_product(client_id, product_id)
        
        if not product_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Produto não encontrado na lista de favoritos do cliente.',
            )
        return self.client_favorite_repository.remove(client_id, product_id)

    def list_favorites(self, client_id):
        client_exist = self.client_repository.get_by_client_id(client_id)

        if not client_exist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário informado não existe.',
            )

        favorites_list = self.client_favorite_repository.get_by_client(client_id)
        if not favorites_list:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Não existe nenhum produto favorito vinculado à este cliente.',
            )
        
        favorites_list_formated = []
        for fav in favorites_list:
            product_data = requests.get(f'https://fakestoreapi.com/products/{fav.product_id}')
            if product_data.status_code != HTTPStatus.OK:
                raise HTTPException(
                    status_code= product_data.status_code,
                    detail='O produto não pode ser validado.'
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

    def is_favorite(self, client_id, item_id):
        """
        Verifica se um item está nos favoritos do cliente.
        """
        return self.client_favorite_repository.is_favorite(client_id, item_id)
    
def get_client_favorite_service(
    client_favorite_repository: ClientFavoriteRepository = Depends(get_client_favorite_repository),
    client_repository: ClientRepository = Depends(get_client_repository)
) -> ClientFavoriteService:
    return ClientFavoriteService(client_favorite_repository, client_repository)
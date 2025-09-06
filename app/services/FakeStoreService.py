from http import HTTPStatus
import json
from fastapi import Depends, HTTPException
from app.repositories.FakeStoreRepository import FakeStoreRepository, get_fake_store_repository
from app.schemas.ProductsSchema import ProductsSchema


class FakeStoreService:
    def __init__(self, fake_store_repository: FakeStoreRepository):
        self.fake_store_repository = fake_store_repository

    def list_products(self):
        products_reponse = self.fake_store_repository.get_all_products()
        if products_reponse.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=products_reponse.status_code,
                detail='Erro ao consultar a lista de produtos.',
            )
        products_list = json.loads(products_reponse.text)
        products_list = [ProductsSchema(
            id=product.get('id'),
            title=product.get('title'),
            image=product.get('image'),
            price=product.get('price'),
            review=product.get('review', ''),
        ) for product in products_list]
        return products_list
    
def get_fake_store_service(
    fake_store_repository: FakeStoreRepository = Depends(get_fake_store_repository)
) -> FakeStoreService:
    return FakeStoreService(fake_store_repository)
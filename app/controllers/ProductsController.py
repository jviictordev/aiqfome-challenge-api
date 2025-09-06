from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.schemas.ProductsSchema import AllProductsSchema
from app.services.FakeStoreService import FakeStoreService, get_fake_store_service

products_router = APIRouter(tags=["Products"])


@products_router.post('/products/list_all', status_code=HTTPStatus.CREATED, response_model=AllProductsSchema)
def list_products(fake_store_service: FakeStoreService = Depends(get_fake_store_service)):
    return fake_store_service.list_products()
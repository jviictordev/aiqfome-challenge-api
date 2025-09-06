from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.schemas.ProductsSchema import AllProductsSchema
from app.services.FakeStoreService import FakeStoreService, get_fake_store_service

products_router = APIRouter(tags=["Products"], prefix='/products')


@products_router.post(
    path='/list_all',
    status_code=HTTPStatus.CREATED,
    response_model=AllProductsSchema,
    summary="Rota para listagem dos produtos da api FakeStore",
    description="Rota pública e qualquer role pode acessar."
)
def list_products(fake_store_service: FakeStoreService = Depends(get_fake_store_service)):
    return fake_store_service.list_products()